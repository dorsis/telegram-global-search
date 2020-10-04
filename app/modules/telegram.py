from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl import functions
import time
from app.config import config
from app.helpers import dictionary, csv_maker

api_id = config.get_data('api_id')
api_hash = config.get_data('api_hash')
username = config.get_data('username')
phone = config.get_data('phone')


class Telegram:
    def __init__(self, query, depth=1):
        self.telegram = TelegramClient(username, api_id, api_hash)
        self.results = {}

        with self.telegram:
            self.telegram.loop.run_until_complete(self.start(query, depth))

    def _add_to_results(self, results):
        added = []

        for channel_id in results:
            if channel_id not in self.results:
                self.results[channel_id] = results[channel_id]

                added.append(results[channel_id])

        return added

    async def _search(self, query, results):
        try:
            time.sleep(3)
            result = await self.telegram(functions.contacts.SearchRequest(
                q=query,
                limit=10000
            ))
        except:
            return

        for channel in result.chats:
            channel_id = channel.id
            channel_username = channel.username
            channel_title = channel.title.replace(',', '/')
            channel_members = channel.participants_count

            if channel_id not in results:
                results[channel_id] = {
                    'id': str(channel_id),
                    'link': f'http://t.me/{channel_username}',
                    'username': channel_username,
                    'title': channel_title,
                    'members_count': str(channel_members)
                }

        results_all = self.results.copy()

        for channel_id in results:
            if channel_id not in results_all:
                results_all[channel_id] = results[channel_id]

        csv_maker.make_csv_file(list(results_all.values()))

    async def _initiate_search_all(self, query, dictionary_words):
        results = {}

        for index, word in enumerate(dictionary_words):
            if query:
                query_word = f'{query} {word}'
            else:
                query_word = word

            print(f'{index + 1}/{len(dictionary_words)} Searching using query: {query_word}')

            if not query_word:
                continue

            await self._search(query_word, results)
            time.sleep(1)

        return results

    def _generate_dictionary_from_results(self, channels, query):
        words_dictionary = []

        for channel in channels:
            channel_title = channel['title']

            words_dictionary += dictionary.generate_words_from_title(channel_title, query)

        return words_dictionary

    async def start(self, query, depth):
        await self.telegram.start()
        # Ensure you're authorized
        if not await self.telegram.is_user_authorized():
            await self.telegram.send_code_request(phone)
            try:
                await self.telegram.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.telegram.sign_in(password=input('Password: '))

        print('Running Initial search')

        results = await self._initiate_search_all(
            query,
            dictionary_words=dictionary.get_words()
        )

        if len(results) == 0:
            return print('No results were found')

        print(f'Initial search found {len(results)}.')

        added_channels = self._add_to_results(results)

        for i in range(depth):
            print('Generating dictionary.')

            dictionary_words = self._generate_dictionary_from_results(added_channels, query)

            print(f'Generated {len(dictionary_words)} query.')

            results = await self._initiate_search_all(None, dictionary_words)

            print(f'Found {len(results)} records at the {i + 1} iteration.')

            added_channels = self._add_to_results(results)


        print(f'Found for all results {len(self.results)} records')

        csv_maker.make_csv_file(list(self.results.values()))
