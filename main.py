# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import leafmap

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting first leafmap test...')
    # center to New York at 41 degrees north and 74 degrees west
    m = leafmap.Map(google_map="HYBRID", center=[40.702557, -74.012318], zoom=12, height="450px",width="800px")  # center=[lat, lon]
    # add a point layer for the taxi data

    # add a chart layer and legends for the taxi statistics

    # show
    m

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
