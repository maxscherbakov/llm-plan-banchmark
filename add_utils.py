import re

def clean_pddl_domain(pddl_text, valid_types):
    def clean_parameters(match):
        action_header = match.group(1)
        params = match.group(2)
        rest = match.group(3)

        cleaned_params = []
        no_name_tokens = []
        tokens = params.strip().split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("?"):
                if i + 2 <= len(tokens) and tokens[i + 1] == "-":
                    var_type = tokens[i + 2]
                    if var_type in valid_types:
                        cleaned_params += [token, "-", var_type]
                    else: 
                        cleaned_params += [token, "-", 'object']
                    i += 3
                else:
                    cleaned_params.append(token)
                    i += 1
            else:
                i += 1

        cleaned_params.extend(no_name_tokens)

        if len(cleaned_params) == 0:
            return ''

        cleaned_params_str = " ".join(cleaned_params)
        return f"(:action {action_header}\n    :parameters ({cleaned_params_str})\n    {rest}\n)"

    pattern = r"\(:action\s+([^\s]+)\s*\n\s*:parameters\s*\((.*?)\)\s*(.*?)\n\s*\)"
    cleaned_pddl = re.sub(pattern, clean_parameters, pddl_text, flags=re.S)

    return cleaned_pddl

def remove_block(pddl_text, remove_block='(:init', new_block='(:init )'):
    start_tag = remove_block
    start_idx = pddl_text.find(start_tag)
    if start_idx == -1:
        return pddl_text
    
    idx = start_idx + len(start_tag)
    stack = 1
    while idx < len(pddl_text) and stack > 0:
        if pddl_text[idx] == "(":
            stack += 1
        elif pddl_text[idx] == ")":
            stack -= 1
        idx += 1

    new_text = pddl_text[:start_idx] + new_block + pddl_text[idx:]
    return new_text

def add_missing_parameters_using_predicates(pddl_text):
    """
    Добавляет недостающие параметры в :parameters, определяя их тип
    по описанию предикатов в (:predicates) без использования regex для поиска переменных в теле действия.
    """
    pred_types = _extract_predicate_types(pddl_text)

    # функция для обработки одного действия
    def process_action(match):
        name = match.group(1)
        params = match.group(2)
        preconditions = match.group(3)
        effect = match.group(4)
        body = preconditions + ':effect' + effect +'\n'

        used_vars = set(re.findall(r"(\?[a-zA-Z0-9_-]+)", body))
        new_params = params.strip()

        declared_types = {mis_var : None for mis_var in used_vars}
        for var, typ in re.findall(r"(\?[a-zA-Z0-9_-]+)\s*-\s*([a-zA-Z0-9_-]+)", new_params):
            declared_types[var] = typ
        
        for id, (var, type) in enumerate(declared_types.items()):
            for pred_name, args in pred_types.items():
                predicates_with_param = _find_predicate_instance(body, pred_name, var)
                if len(predicates_with_param) > 0:
                    vars = predicates_with_param[0]
                    id_var = predicates_with_param[0].index(var)
                    found_type = args[id_var][1]
                    if type != found_type:
                        new_obj = f'?{found_type}_{id}'
                        new_predicate_vars = vars.copy()
                        new_predicate_vars[id_var] = new_obj
                        new_params += f" {new_obj} - {found_type}"
                        old_pattern = r"\(\s*" + re.escape(pred_name) + r"\s+" + r"\s+".join(map(re.escape, vars)) + r"\s*\)"
                        new_text = f"({pred_name} {' '.join(new_predicate_vars)})"
                        body, _ = re.subn(old_pattern, new_text, body)
                        
        return f"(:action {name}\n        :parameters ({new_params})\n        {body}"
    
    pattern = r"\(:action\s+([^\s]+)\s*\n\s*:parameters\s*\((.*?)\)\s*(.*?):effect\s*(.*?)\s*\n"
    return re.sub(pattern, process_action, pddl_text, flags=re.S)

def _extract_predicates_block(pddl_text):
    """Извлекает блок (:predicates ...) с учётом вложенных скобок."""
    start = pddl_text.find("(:predicates")
    if start == -1:
        return None

    depth = 0
    end = None
    for i in range(start, len(pddl_text)):
        if pddl_text[i] == "(":
            depth += 1
        elif pddl_text[i] == ")":
            depth -= 1
            if depth == 0:
                end = i
                break

    if end:
        return pddl_text[start:end + 1]
    return None

def _extract_predicate_types(pddl_text):
    """
    Извлекает типы аргументов из блока (:predicates)
    Возвращает словарь:
      { 'pred_name': [(var, type), ...] }
    """
    preds = {}
    block = _extract_predicates_block(pddl_text)
    if not block:
        return preds

    # Находим все предикаты (имя и список аргументов)
    pred_matches = re.findall(r"\(([a-zA-Z0-9_-]+)([^()]*)\)", block)
    for pred_name, args_str in pred_matches:
        tokens = args_str.strip().split()
        args = []
        i = 0
        while i < len(tokens):
            if tokens[i].startswith("?"):
                if i + 2 <= len(tokens) and tokens[i + 1] == "-":
                    args.append((tokens[i], tokens[i + 2]))
                    i += 3
                else:
                    args.append((tokens[i], None))
                    i += 1
            else:
                i += 1
        preds[pred_name] = args

    return preds

def _find_predicate_instance(body, pred_name, var):
    """
    Ищет в тексте body предикат pred_name, где встречается переменная var.
    Возвращает список всех аргументов этого предиката.
    """
    def tokenize_pddl(s):
        tokens = []
        token = ""
        for c in s:
            if c in " \t\n":
                if token:
                    tokens.append(token)
                    token = ""
            elif c in "()":
                if token:
                    tokens.append(token)
                    token = ""
                tokens.append(c)
            else:
                token += c
        if token:
            tokens.append(token)
        return tokens

    tokens = tokenize_pddl(body)
    instances = []

    i = 0
    while i < len(tokens):
        if tokens[i] == '(' and i + 1 < len(tokens) and tokens[i+1] == pred_name:
            # нашли предикат, теперь собираем его аргументы
            args = []
            depth = 1
            j = i + 2
            while j < len(tokens) and depth > 0:
                if tokens[j] == '(':
                    depth += 1
                elif tokens[j] == ')':
                    depth -= 1
                if depth > 0:
                    args.append(tokens[j])
                j += 1
            # проверяем, есть ли нужная переменная
            if var in args:
                instances.append(args)
            i = j
        else:
            i += 1

    return instances
