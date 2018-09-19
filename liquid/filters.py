__all__ = ['filters']

def _abs(val):
	if not isinstance(val, int) and not isinstance(val, float):
		if val.isdigit() or (val[0] in ['+', '-'] and val[1:].isdigit()):
			return abs(int(val))
		else:
			return abs(float(val))
	return abs(val)

def _date(val, outformat, informat = None):
	from datetime import datetime
	if val == 'now':
		return datetime.now().strftime(outformat)
	if val == 'today':
		return datetime.today().strftime(outformat)
	return datetime.strptime(val, informat).strftime(outformat)

def _truncatewords(val, l, end = '...'):
	words = val.split()
	if len(words) <= l:
		return words
	return ' '.join(words[:l]) + end

def _split(val, sep, limit = -1):
	if sep:
		return val.split(sep, limit)
	if limit < 0 or limit >= len(val):
		return list(val)
	if limit == 0:
		return [val]
	val = list(val)
	return val[:(limit - 1)] + ''.join(val[limit:])

filters = dict(
	abs        = _abs,
	append     = lambda x, y: str(x) + str(y),
	capitalize = lambda x: str(x).capitalize(),
	prepend    = lambda x, y: str(y) + str(x),
	at_least   = min,
	at_most    = max,
	ceil       = lambda x: __import__('math').ceil(float(x)),
	compact    = lambda x: list(filter(None, x)),
	map        = lambda x, y: [getattr(v, y) for v in x],
	concat     = lambda x, y: x + y,
	split      = _split,
	date       = _date,
	default    = lambda x, y: x or y,
	divided_by = lambda x, y: x / y,
	times      = lambda x, y: x * y,
	downcase   = lambda x: str(x).lower(),
	escape     = lambda x, quote = True: __import__('cgi').escape(x, quote),
	floor      = lambda x: __import__('math').floor(float(x)),
	join       = lambda x, y: y.join(x),
	lstrip     = lambda x: str(x).lstrip(),
	minus      = lambda x, y: x - y,
	modulo     = lambda x, y: x % y,
	mod        = lambda x, y: x % y,
	newline_to_br = lambda x: x.replace('\n', '<br />'),
	nl2br      = lambda x: x.replace('\n', '<br />'),
	plus       = lambda x, y: x + y,
	remove     = lambda x, y, z = -1: str(x).replace(str(y), '', z),
	remove_first = lambda x, y: str(x).replace(str(y), '', 1),
	replace = lambda x, y, z, w = -1: str(x).replace(str(y), str(z), w),
	replace_first = lambda x, y, z: str(x).replace(str(y), str(z), 1),
	reverse    = lambda x: x[::-1],
	round      = lambda x, n = 0: round(float(x), n),
	rstrip     = lambda x: str(x).rstrip(),
	size       = len,
	slice      = lambda x, y, z = 1: x[y:(z if not z else z - y if y < 0 else z + y)],
	sort       = lambda x: list(sorted(x)),
	strip      = lambda x: str(x).strip(),
	strip_html = lambda x: __import__('re').sub(r'<.*?>', '', x),
	strip_newlines = lambda x: x.replace('\n', ''),
	truncate   = lambda x, y, z = '...': x if len(x) + len(z) <= y else x[:(y - len(z))] + z,
	truncatewords = _truncatewords,
	uniq       = lambda x: list(set(x)),
	upcase     = lambda x: str(x).upper(),
	url_encode = lambda x: __import__('urllib').urlencode({'': x})[1:],
	url_decode = lambda x: __import__('urllib').unquote(x)
)