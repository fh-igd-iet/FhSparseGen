#!/usr/bin/env python3

"""
FhSparseGen – Fraunhofer Sparse Matrix Layout Generator for Compound Entries

The Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung e.V., Hansastrasse 27c, 80686 Munich, Germany (further: Fraunhofer) is holder of all proprietary rights on this computer program.

Copyright©2019 Gesellschaft zur Förderung der angewandten Forschung e.V. acting on behalf of its Fraunhofer Institut für Graphische Datenverarbeitung. All rights reserved.

Contact: andre.stork@igd.fraunhofer.de
"""

def is_valid_identifier(identifier):
    """
    Checks if the given identifier is a valid C identifier
    """

    import re

    # check character set
    if identifier != identifier.strip() or not re.match('^[a-zA-Z_][a-zA-Z0-9_]+$', identifier):
        return False

    # reserved keywords source: http://en.cppreference.com/w/cpp/keyword
    reserved_keywords = set([
        'alignas',
        'alignof',
        'and',
        'and_eq',
        'asm',
        'atomic_cancel',
        'atomic_commit',
        'atomic_noexcept',
        'auto',
        'bitand',
        'bitor',
        'bool',
        'break',
        'case',
        'catch',
        'char',
        'char16_t',
        'char32_t',
        'class',
        'compl',
        'concept',
        'const',
        'constexpr',
        'const_cast',
        'continue',
        'decltype',
        'default',
        'delete',
        'do',
        'double',
        'dynamic_cast',
        'else',
        'enum',
        'explicit',
        'export',
        'extern',
        'false',
        'float',
        'for',
        'friend',
        'goto',
        'if',
        'import',
        'inline',
        'int',
        'long',
        'module',
        'mutable',
        'namespace',
        'new',
        'noexcept',
        'not',
        'not_eq',
        'nullptr',
        'operator',
        'or',
        'or_eq',
        'private',
        'protected',
        'public',
        'register',
        'reinterpret_cast',
        'requires',
        'return',
        'short',
        'signed',
        'sizeof',
        'static',
        'static_assert',
        'static_cast',
        'struct',
        'switch',
        'synchronized',
        'template',
        'this',
        'thread_local',
        'throw',
        'true',
        'try',
        'typedef',
        'typeid',
        'typename',
        'union',
        'unsigned',
        'using',
        'virtual',
        'void',
        'volatile',
        'wchar_t',
        'while',
        'xor',
        'xor_eq'
    ])

    if identifier in reserved_keywords:
        return False

    # identifiers with two consecutive underscores are reserved
    if '__' in identifier:
        return False

    # identifiers beginning with an underscore are reserved in the global namespace
    if identifier.startswith('_'):
        return False

    # identifiers ending in _t are reserved in POSIX
    if identifier.endswith('_t'):
        return False

    return True

def is_valid_index_type(index_type):
    """
    Checks if the index_type is a valid C/C++ integrated integer type
    """
    from itertools import product

    if index_type != index_type.strip():
        return False

    valid_index_types = []

    intrinsic_parts = [
        ['unsigned ', 'signed ', ''],
        ['char', 'short', 'int', 'long', 'long long']
    ]
    for elts in product(*intrinsic_parts):
        valid_index_types.append(''.join(elts))
    valid_index_types.append('unsigned')
    valid_index_types.append('signed')

    sized_parts = [
        ['std::', ''],
        ['int', 'uint'],
        ['', '_fast', '_least'],
        ['8_t', '16_t', '32_t', '64_t']
    ]
    for elts in product(*sized_parts):
        valid_index_types.append(''.join(elts))

    max_ptr_parts = [
        ['std::', ''],
        ['int', 'uint'],
        ['max_t', 'ptr_t']
    ]
    for elts in product(*max_ptr_parts):
        valid_index_types.append(''.join(elts))

    size_diff_parts = [
        ['std::', ''],
        ['size_t', 'ptrdiff_t']
    ]
    for elts in product(*size_diff_parts):
        valid_index_types.append(''.join(elts))

    valid_index_types = set(valid_index_types)

    return index_type in valid_index_types

def deduplicated_sizeof(member_list):
    """
    Converts a list of identifiers with duplicates such as ['double', 'int', 'double']
    to an expression such as '(2 * sizeof(double) + sizeof(int))'.
    """
    from collections import Counter

    member_list = list(member_list)
    if not member_list:
        return '0'

    member_counts = Counter(member_list)
    result = ' + '.join(
        ('' if member_counts[key] == 1 else '{} * '.format(member_counts[key])
        ) + 'sizeof({})'.format(key) for key in sorted(member_counts)
    )
    result = '({})'.format(result) if len(member_counts) > 1 else result
    return result

def indent_tab(text, num_tabs=1):
    """
    Indent using tabs
    """
    ret = ''
    first = True
    for elt in text.split('\n'):
        if not first:
            ret += '\n'
        if elt.strip() and not first:
            ret += num_tabs * '\t'
        ret += elt
        first = False
    return ret

def compute_size(members):
    type_to_size = {
        'float': 4,
        'double': 8,
    }
    return sum(type_to_size[member['type']] for member in members)

def compute_alignment(members):
    size = compute_size(members)
    for alignment in [2, 4, 8, 16][::-1]:
        if size % alignment == 0:
            return alignment
    return 1

def run():
    """
    Sparse matrix generation runner implementation
    """
    import os
    import sys
    import jinja2 as j2
    import argparse as ap

    template_path = os.path.dirname(os.path.realpath(__file__))
    template_loader = j2.FileSystemLoader(searchpath=template_path)
    template_env = j2.Environment(
        loader=template_loader,
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=j2.StrictUndefined
    )
    template_env.filters['deduplicated_sizeof'] = deduplicated_sizeof
    template_env.filters['indent_tab'] = indent_tab
    template_env.filters['unique'] = lambda x: sorted(set(x))

    parser = ap.ArgumentParser()
    parser.add_argument('--value-name', type=str, default='Complex')
    parser.add_argument('--vector-name', type=str)
    parser.add_argument('--matrix-name', type=str)
    parser.add_argument('--header-name', type=str)
    parser.add_argument('--source-name', type=str)
    parser.add_argument('--index-type', type=str, default='int')
    parser.add_argument('--cuda', action='store_true')
    parser.add_argument('--members', type=str, default='real:float,imag:float')
    parser.add_argument('--omp-schedule', type=str, default='dynamic', choices=[
        'static', 'dynamic', 'guided'
    ])
    parser.add_argument('--omp-chunk-size', type=int)
    parser.add_argument('--cuda-schedule', type=str, default='static', choices=[
        'static', 'dynamic'
    ])
    parser.add_argument('--cuda-blocks', type=int, default=64)
    parser.add_argument('--cuda-threads', type=int, default=256)
    parser.add_argument('--inner', type=str, default='interleaved', choices=[
        'interleaved', 'noninterleaved'
    ])
    parser.add_argument('--vector-layout', type=str, choices=[
        'interleaved', 'noninterleaved'
    ])
    parser.add_argument('--outer', type=str, default='csr', choices=['csr', 'transposed', 'blocked'])
    parser.add_argument('--mac-template', dest='multiply_accumulate_template', type=str, default=(
        "r.real += a.real * b.real - a.imag * b.imag;" +
        "r.imag += a.real * b.imag + a.imag * b.real;"
    ))
    parser.add_argument('--zero-template', dest='zero_initialize_template', type=str, default=(
        "r.real = -0.;" +
        "r.imag = -0.;"
    ))
    parser.add_argument('--blockSize', type=int, default=16, choices=[8, 16, 32, 64])
    parser.add_argument('--vector-value-name', type=str)
    parser.add_argument('--vector-members', type=str)
    parser.add_argument('--vector-zero-template', type=str, dest='vector_zero_initialize_template')
    parser.add_argument('--cuda-blocks-per-mp', type=int, default=2)
    args = parser.parse_args()

    if args.vector_value_name is None:
        args.vector_value_name = args.value_name
    if args.vector_name is None:
        args.vector_name = '{}Vector'.format(args.vector_value_name)
    if args.matrix_name is None:
        args.matrix_name = '{}Matrix'.format(args.value_name)
    if args.header_name is None:
        args.header_name = '{}.hpp'.format(args.matrix_name)
    if args.source_name is None:
        args.source_name = ('{}.cu' if args.cuda else '{}.cpp').format(args.matrix_name)
    if not is_valid_index_type(args.index_type):
        print('"{}" is not a valid index type'.format(args.index_type))#, file=sys.stderr)
        exit(1)
    args.members = [
        {'name': a.strip(), 'type': b.strip()} for a, b in (
            e.split(':') for e in args.members.split(',')
        )
    ]
    if args.vector_members is None:
        args.vector_members = args.members
    else:
        args.vector_members = [
            {'name': a.strip(), 'type': b.strip()} for a, b in (
                e.split(':') for e in args.vector_members.split(',')
            )
        ]
    args.alignment = compute_alignment(args.members)
    args.vector_alignment = compute_alignment(args.vector_members)

    if args.vector_layout is None:
        args.vector_layout = args.inner

    args.scheduling = {
        'cuda' : {
            'schedule': args.cuda_schedule,
            'blocks' : args.cuda_blocks,
            'threads' : args.cuda_threads,
            'blocks_per_mp' : args.cuda_blocks_per_mp,
        },
        'omp' : {
            'schedule' : args.omp_schedule,
            'chunk_size' : args.omp_chunk_size,
        }
    }
    del args.cuda_schedule, args.cuda_blocks, args.omp_chunk_size, args.omp_schedule, args.cuda_blocks_per_mp

    args.multiply_accumulate_template = ';\n'.join(
        map(str.strip, args.multiply_accumulate_template.split(';'))
    ).rstrip()
    args.zero_initialize_template = ';\n'.join(
        map(str.strip, args.zero_initialize_template.split(';'))
    ).rstrip()
    if args.vector_zero_initialize_template is None:
        args.vector_zero_initialize_template = args.zero_initialize_template
    else:
        args.vector_zero_initialize_template = ';\n'.join(
            map(str.strip, args.vector_zero_initialize_template.split(';'))
        ).rstrip()

    argsd = vars(args)
    for fname, tname in [
            (args.header_name, 'header.j2'),
            (args.source_name, 'source.j2')
    ]:
        text = template_env.get_template(tname).render(**argsd)
        with open(fname, 'w') as out_file:
            out_file.write(text)

if __name__ == '__main__':
    run()
