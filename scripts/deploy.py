from src.scripts.lottery import deploy_lottery, end_lottery, enter_lottery, start_lottery


def main():
    deploy_lottery()
    print('lottery was successfully deployed!')

    _ = start_lottery()
    print('lottery has started!')
    _ = enter_lottery()
    print('successfully entered lottery!')

    end_lottery()
