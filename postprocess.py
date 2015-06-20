import logging
from argparse import ArgumentParser

DEFAULT_INPUT = 'output/result.arff'  # my input is the output of weka
DEFAULT_OUTPUT = 'output/result.csv'

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.INFO)

    """
    Read non-default input paths from args
    """

    argparser = ArgumentParser(description='Convert arff from weka to csv.')
    argparser.add_argument('-i', '--input', default=DEFAULT_INPUT,
                           help='input file (arff format)')
    argparser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                           help='output file (csv format)')
    args = argparser.parse_args()

    """
    Read arff file and convert it to a csv file with only id and class
    """

    out = open(args.output, 'w')
    out.write('id;video_category_id\n')

    with open(args.input) as f:
        skip = True
        for line in f:
            if skip:
                if '@data' in line:
                    skip = False
            else:
                r = line.split(',')
                test_id = r[0]
                test_predicted = r[-2]

                out.write(test_id + ';' + test_predicted + '\n')
