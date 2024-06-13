def is_valid_iidx_id(iidx_id):
    return iidx_id.isdigit() and len(iidx_id) == 8


def validate_inputs(iidx_id_me, iidx_ids, num_rivals):
    errors = []
    valid = True
    if not is_valid_iidx_id(iidx_id_me):
        errors.append('自分のIIDX IDは8桁の数字でなければなりません。')
        valid = False
    for i in range(1, num_rivals + 1):
        if not is_valid_iidx_id(iidx_ids[f'rival{i}']):
            errors.append(f'比較したい人のIIDX ID {i} は8桁の数字でなければなりません。')
            valid = False
    return valid, errors
