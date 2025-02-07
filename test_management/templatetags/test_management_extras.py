from django import template
from collections import defaultdict

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """辞書からキーに対応する値を取得するフィルター"""
    return dictionary.get(key)

@register.filter
def subtract(value, arg):
    """引き算を行うフィルター"""
    return value - len(arg)

@register.filter
def count_by_status(results, status):
    """特定のステータスの結果数を集計するフィルター"""
    if not results:
        return 0
    return sum(1 for result in results.values() if result.status == status) 