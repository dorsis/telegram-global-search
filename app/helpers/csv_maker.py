from app.config import config

csv_file = config.get_data('csv_file')


def make_csv_file(data):
    with open(csv_file, 'w') as file:
        if len(data) == 0:
            return

        keys = ','.join(list(data[0].keys()))

        file.write(keys + '\n')

        for record in data:
            try:
                file.write(','.join(list(record.values())) + '\n')
            except:
                pass

    print(f'File saved to {csv_file}')
