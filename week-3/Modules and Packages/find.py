import sys, os
import datetime

def parse_options(args):
    options = {
        "name":None,
        "atime":None,
        "type":'f',
        "maxdepth":1,
        'search_dir':'.'
    }
    i=0

    while i<len(args):
        arg = args[i]
        if arg.startswith('-'):
            if arg in ['-n', '-name']:
                i+=1
                if i<len(args):
                    options['name'] = args[i]
            
            elif arg in ['-atime']:
                i+=1
                if i<len(args):
                    try:
                        options['atime'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid time value: {args[i]}")
                        sys.exit(1)

                
            elif arg in ['-t', '-type']:
                i+=1
                if i<len(args):
                    try:
                        if args[i].lower() not in ['f', 'd']:
                            raise ValueError()
                        options['type'] = args[i].lower()
                    except ValueError:
                        print(f'Invalid file type: {args[i]}. Try again with "f" or "d"')
                        sys.exit(1)
                        

                
            elif arg in ['-m', '--max-depth']:
                i+=1
                if i<len(args):
                    try:
                        options['maxdepth'] = int(args[i])
                    except ValueError:
                        print(f"Error: Invalid depth value: {args[i]}")
                        sys.exit(1)

            else:
                print(f"Error: Unknown option: {arg}")
                sys.exit(1)
        
        else:
            options['search_dir'] = args[i]
        i+=1

    if not options['name']:
        print("Please provide a file name with -n -name option")
        sys.exit(1)
    
    return options


def matchFile(file_path, options):
    file_name = os.path.basename(file_path)
    if options['name'] not in file_name: 
        return False

    is_file = os.path.isfile(file_path)
    if options['type']=='f' and not is_file or options['type']=='d' and is_file or not options['type']:
        return False
    
    if options['atime']:
        last_access = datetime.datetime.fromtimestamp(os.path.getatime(file_path))
        days_since_access = (datetime.datetime.now() - last_access).days
        if days_since_access>options['atime']:
            return False

    return True


def traverse(curr_dir, curr_depth, options):
    if curr_depth <= options['maxdepth']:
        try:
            for entry in os.listdir(curr_dir):
                entry_path = os.path.join(curr_dir, entry)
                
                if matchFile(entry_path, options):
                    print(entry_path)

                if os.path.isdir(entry_path):
                    traverse(entry_path, curr_depth+1, options)
        except (PermissionError, OSError):
            pass



def find(options):
    search_dir = options['search_dir']
    traverse(search_dir, 1, options)


if __name__ == '__main__':
    options = parse_options(sys.argv)
    find(options)