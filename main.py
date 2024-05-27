import argparse

def main():
    parser = argparse.ArgumentParser(description='Cache simulation script.')
    parser.add_argument('test_file', type=str, help='Path to the test file')
    parser.add_argument('--cache_size', type=int, required=True, help='Cache size in bytes')
    parser.add_argument('--num_blocks_per_set', type=int, required=True, help='Number of blocks per set')
    parser.add_argument('--block_size', type=int, required=True, help='Block size in bytes')
    parser.add_argument('--pipelined', type=int, choices=[1, 2], required=True, help='1 for pipelined, 2 for non-pipelined')
    parser.add_argument('--forwarding', type=int, choices=[1, 2], help='1 for forwarding, 2 for not-forwarding (only for pipelined)')
    parser.add_argument('--print_registers', type=int, choices=[1, 2], help='1 for printing registers, 2 for not (only for pipelined)')

    args = parser.parse_args()

    cacheSize = args.cache_size
    numBlocksPerSet = args.num_blocks_per_set
    blockSize = args.block_size
    numSet = cacheSize // (blockSize * numBlocksPerSet)

    if args.pipelined == 1:
        from pipelined.control import Control
        control = Control(numSet, numBlocksPerSet, blockSize, cacheSize)

        if args.forwarding == 1:
            control.forwarding = True
        else:
            control.forwarding = False

        if args.print_registers == 1:
            control.print_registers = True
        else:
            control.print_registers = False

    else:
        from non_pipelined.control import Control

        control = Control(numSet, numBlocksPerSet, blockSize, cacheSize)

    # Load the test file
    control.load(args.test_file)

    # Run the simulation
    control.run()

    # Dump the results to a file
    control.dump()

if __name__ == '__main__':
    main()
