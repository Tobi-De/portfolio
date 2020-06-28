def queryset_index_of(queryset, value):
    for index, obj in enumerate(queryset):
        if value == obj:
            return index
