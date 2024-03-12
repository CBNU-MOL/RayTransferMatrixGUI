def pair_lines_by_style(y_values, line_styles):
    # 광선 스타일을 기준으로 광선 인덱스 그룹화
    style_groups = {}
    for index, style in enumerate(line_styles):
        style_key = tuple(style)  # 스타일 정보를 튜플로 변환하여 해시 가능하게 만듬
        if style_key in style_groups:
            style_groups[style_key].append(index)
        else:
            style_groups[style_key] = [index]

    # 동일한 스타일을 공유하는 광선들의 인덱스를 짝지어 리스트로 만듬
    paired_indices = []
    for group in style_groups.values():
        # 그룹 내의 모든 인덱스에 대해, 가능한 모든 짝을 만듬
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                paired_indices.append((group[i], group[j]))

    return paired_indices

# 주어진 광선 Y 값과 스타일 정보
y_values = [-0.25, 0.25, -4.356656521801906, -5.445820652252382, -3.2674923913514293, 4.356656521801906, 5.445820652252382, 3.2674923913514293]
line_styles = [((0.0, 0.5, 0.0, 1), '-'), ((0.0, 0.5, 0.0, 1), '-'), ((1.0, 0.0, 0.0, 1), '-'), ('r', '--'), ('r', '--'), ((0.0, 0.0, 1.0, 1), '-'), ('b', '--'), ('b', '--')]

# 함수 호출
paired_indices = pair_lines_by_style(y_values, line_styles)
print(paired_indices)
