from util.dynamic_loader import create

def main():
    chapter = 'ch01'
    before_result = create(f'{chapter}.before', 'main')()
    after_result = create(f'{chapter}.after', 'main')()
    if before_result != after_result:
        raise ValueError
    else:
        return 'Sucess'

if __name__ == '__main__':
    print(main())