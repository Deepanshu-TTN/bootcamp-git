import sys

def parse_args(args):
    options = {
        'file': None,
        'delimiter': None,
        'quotechar': '"',
        'fields': None,
        'skip_rows': 0,
        'head': None,
        'tail': None
    }
    i = 1
    while i < len(args):
        arg = args[i]
        
        if arg.startswith('-'):
            if arg in ['-d', '--delimiter']:
                i += 1
                if i < len(args):
                    options['delimiter'] = args[i]
            elif arg in ['-q', '--quotechar']:
                i += 1
                if i < len(args):
                    options['quotechar'] = args[i]
            elif arg in ['-f', '--fields']:
                i += 1
                if i < len(args):
                    try:
                        options['fields'] = [int(x) for x in args[i].split(',')]
                    except ValueError:
                        print(f"Error: Invalid field numbers: {args[i]}")
                        sys.exit(1)
            elif arg == '--skip-rows':
                i += 1
                if i < len(args):
                    try:
                        options['skip_rows'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid skip rows value: {args[i]}")
                        sys.exit(1)
            elif arg == '--head':
                i += 1
                if i < len(args):
                    try:
                        options['head'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid head value: {args[i]}")
                        sys.exit(1)
            elif arg == '--tail':
                i += 1
                if i < len(args):
                    try:
                        options['tail'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid tail value: {args[i]}")
                        sys.exit(1)
            else:
                print(f"Error: Unknown option: {arg}")
                sys.exit(1)
        else:
            options['file'] = arg
        i += 1
    
    if not options['file']:
        print("Error: No input file specified")
        sys.exit(1)
    
    return options

def guess_delimiter(first_line):
    delimiters = [',', ';', '\t', '|']
    counts = {}
    for d in delimiters:
        counts[d] = first_line.count(d)
    
    max_count = 0
    chosen_delimiter = ','
    for d, count in counts.items():
        if count > max_count:
            max_count = count
            chosen_delimiter = d
    
    return chosen_delimiter

def parse_quoted_line(line, delimiter, quote_char):
    result = []
    current_field = []
    in_quotes = False
    
    for char in line:
        if char == quote_char:
            in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:
            result.append(''.join(current_field).strip())
            current_field = []
        else:
            current_field.append(char)
    
    result.append(''.join(current_field).strip())
    return result

def get_column_widths(headers, data):
    """Calculate uniform column widths."""
    widths = []
    for i in range(len(headers)):
        width = len(headers[i])
        for row in data:
            if i < len(row):
                width = max(width, len(row[i]))
        widths.append(width)
    return widths

def print_separator(widths):
    parts = []
    for w in widths:
        parts.append('-' * w)
    print('+-%s-+' % '-+-'.join(parts))

def print_row(row, widths):
    parts = []
    for i, value in enumerate(row):
        if i < len(widths):
            parts.append(value.ljust(widths[i]))
    print('| %s |' % ' | '.join(parts))


def process_file(options):
    """Process the CSV file and display the formatted output."""
    try:
        with open(options['file'], 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            
            delimiter = options['delimiter'] or guess_delimiter(lines[0])
            
            headers = parse_quoted_line(lines[0], delimiter, options['quotechar'])
            
            data_start = 1 + options['skip_rows']
            data_lines = lines[data_start:]
            
            if options['head'] is not None:
                data_lines = data_lines[:options['head']]
            elif options['tail'] is not None:
                data_lines = data_lines[-options['tail']-options['skip_rows']:-options['skip_rows']]
            
            data = [parse_quoted_line(line, delimiter, options['quotechar']) 
                   for line in data_lines if line.strip()]
            
            if options['fields']:
                field_indices = [i - 1 for i in options['fields']]
                headers = [headers[i] for i in field_indices if i < len(headers)]
                filtered_data = []
                for row in data:
                    filtered_row = [row[i] for i in field_indices if i < len(row)]
                    filtered_data.append(filtered_row)
                data = filtered_data
            
            widths = get_column_widths(headers, data)
            
            print_separator(widths)
            print_row(headers, widths)
            print_separator(widths)
            
            for row in data:
                print_row(row, widths)
            
            print_separator(widths)
            
    except FileNotFoundError:
        print(f"Error: File '{options['file']}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    options = parse_args(sys.argv)
    process_file(options)

if __name__ == "__main__":
    main()
