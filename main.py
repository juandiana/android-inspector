import argparse
from components import repositories_manager
from model.operation import Operation
from helpers.operations_helpers import create_operation_folders


def main():
    parser = argparse.ArgumentParser(description='Extracts Android logs or application packages')
    parser.add_argument('--log', help='extract a log')
    parser.add_argument('--app', help='extract an application package')
    parser.add_argument('--devinfo', help='specify device info')
    args = parser.parse_args()

    # Control input
    if not (args.log or args.app):
        parser.error('One of --app or --log is required.')
    elif not args.devinfo:
        parser.error('You must specify the device info. Use --devinfo')

    if args.log:
        print 'Not implemented yet!'
    else:
        operation_dir = create_operation_folders('tmp/')

        extractor = repositories_manager.get_extractor('ApplicationExtractor')
        inspector = repositories_manager.get_inspector('EmailMessageInspector')
        op = Operation(extractor, inspector, {'package_name': args.app})

        op.execute(args.devinfo, operation_dir)


if __name__ == "__main__":
    main()
