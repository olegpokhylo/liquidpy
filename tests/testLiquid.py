from liquid import Liquid
import testly, logging

Liquid.LOGLEVEL = logging.DEBUG
Liquid.DEFAULT_MODE = 'compact'

class TestLiquid(testly.TestCase):

	def dataProvider_testRender(self):
		yield '{{ page.title }}', {'page': testly.Box(title = 'Introduction')}, 'Introduction'
		yield '''{% if user %}
Hello {{ user.name }}!{% endif %}''', {'user': testly.Box(name = 'Adam')}, 'Hello Adam!'
		yield '''{% if product.title == "Awesome Shoes" %}
  These shoes are awesome!{% endif %}''', {'product': testly.Box(title = 'Awesome Shoes')}, '  These shoes are awesome!'
		yield '''{% if product.type == "Shirt" or product.type == "Shoes" %}
  This is a shirt or a pair of shoes.{% endif %}''', {'product': testly.Box(type = 'Shirt')}, '''  This is a shirt or a pair of shoes.'''
		# python 'in' used instead of liquid 'contains'
		yield '''{% if 'Pack' in product.title %}
  This product's title contains the word Pack.{% endif %}''', {'product': testly.Box(title = 'whateverPack')}, '  This product\'s title contains the word Pack.'
		yield '''{% if 'Hello' in product.tags %}
  This product has been tagged with 'Hello'.{% endif %}''', {'product': testly.Box(tags = '23Hello234')}, "  This product has been tagged with 'Hello'."
	
		yield '''{% assign tobi = "Tobi" %}

{% if tobi %}
  This condition will always be true.
{% endif %}''', {}, '''
  This condition will always be true.
'''

		# different truthy from liquid
		# see: https://shopify.github.io/liquid/basics/truthy-and-falsy/
		yield '''{% if settings.fp_heading %}
  <h1>{{ settings.fp_heading }}</h1>{% endif %}''', {'settings': testly.Box(fp_heading = 1)}, '  <h1>1</h1>'

		yield '{% assign my_string = "Hello World!" %}{{my_string}}', {}, 'Hello World!'
		yield '{% assign my_int = 25 %}{{my_int}}', {}, '25'
		# 10
		yield '{% assign my_float = 39.756 %}{{my_float}}', {}, '39.756'
		yield '{% assign foo = true %}{% if foo %}true{% else %}false{% endif %}', {}, 'true'
		yield '{% assign foo = false %}{% if foo %}true{% else %}false{% endif %}', {}, 'false'
		yield '{% assign foo = nil %}{% if foo %}true{% else %}false{% endif %}', {}, 'false'

		# whitespace controls
		yield '''{% mode loose %}
{% assign my_variable = "tomato" %}
{{ my_variable }}''', {}, '''
tomato'''
		yield '''{% mode loose %}
{%- assign my_variable = "tomato" -%}
{{ my_variable }}''', {}, 'tomato'
		yield '''{% assign username = "John G. Chalmers-Smith" %}
{% if username and len(username) > 10 %}
  Wow, {{ username }}, you have a long name!
{% else %}
  Hello there!
{% endif %}
''', {}, '  Wow, John G. Chalmers-Smith, you have a long name!\n'
		yield '''{%- assign username = "John G. Chalmers-Smith" -%}
{%- if username and len(username) > 10 -%}
  Wow, {{ username }}, you have a long name!
{%- else -%}
  Hello there!
{%- endif -%}
''', {}, '  Wow, John G. Chalmers-Smith, you have a long name!\n'

		# comments
		yield '''Anything you put between {% comment %} and {% endcomment %} tags
is turned into a comment.''', {}, '''Anything you put between# andtags
is turned into a comment.'''
		yield '''Anything you put between {# and #} tags
is turned into a comment.''', {}, '''Anything you put betweentags
is turned into a comment.'''

		#20
		# unless
		yield '''{% unless product.title == 'Awesome Shoes' %}
  These shoes are not awesome.
{% endunless %}''', {'product': testly.Box(title = 'Notawesome Shoes')}, '''  These shoes are not awesome.
'''
		# elsif
		yield '''{% if customer.name == 'kevin' %}
  Hey Kevin!
{% elsif customer.name == 'anonymous' %}
  Hey Anonymous!
{% else %}
  Hi Stranger!
{% endif %}''', {'customer': testly.Box(name = 'anonymous')}, '''  Hey Anonymous!
'''

		# case / when
		yield '''{% assign handle = 'cake' %}
{% case handle %}
  {% when 'cake' %}
     This is a cake
  {% when 'cookie' %}
     This is a cookie
  {% else %}
     This is not a cake nor a cookie
{% endcase %}''', {}, '''     This is a cake
'''

		yield '''{% for product in collection.products %}
{{ product.title }}
{% endfor %}''', {'collection': testly.Box(
	products = [
		testly.Box(title = 'hat'), 
		testly.Box(title = 'shirt'), 
		testly.Box(title = 'pants')
	])}, '''hat
shirt
pants
'''

		yield '''{% for i in range(1, 6) %}
  {% if i == 4 %}
    {% break %}
  {% else %}
    {{ i }}
  {% endif %}
{% endfor %}''', {}, '''    1
    2
    3
'''

		yield '''{% for i in range(1, 6) %}
  {% if i == 4 %}
    {% continue %}
  {% else %}
    {{ i }}
  {% endif %}
{% endfor %}''', {}, '''    1
    2
    3
    5
'''

		yield '''{% raw %}
  In Handlebars, {{ this }} will be HTML-escaped, but
  {{{ that }}} will not.
{% endraw %}''', {}, '''  In Handlebars, {{ this }} will be HTML-escaped, but
  {{{ that }}} will not.
'''
		# assign
		yield '''{% assign my_variable = false %}
{% if my_variable != true %}
  This statement is valid.
{% endif %}''', {}, '  This statement is valid.\n'
		yield '''{% assign foo = "bar" %}
{{ foo }}''', {}, '''bar'''

		# capture
		yield '''{% capture my_variable %}I am being captured.{% endcapture %}
{{ my_variable }}''', {}, 'I am being captured.'

		# capture
		yield '''{% assign favorite_food = 'pizza' %}
{% assign age = 35 %}

{% capture about_me %}
I am {{ age }} and my favorite food is {{ favorite_food }}.
{% endcapture %}

{{ about_me }}''', {}, '\n\nI am 35 and my favorite food is pizza.\n'

		# in/decrement
		yield '''{% increment my_counter %}
		{{ my_counter }}
		{% increment my_counter %}
		{{ my_counter }}
		{% increment my_counter %}
		{{ my_counter }}''', {'my_counter': 0}, '''		1
		2
		3''' 

		yield '''{% decrement my_counter %}
		{{ my_counter }}
		{% decrement my_counter %}
		{{ my_counter }}
		{% decrement my_counter %}
		{{ my_counter }}''', {'my_counter': 0}, '''		-1
		-2
		-3''' 

		# filters
		yield '{{ -17 | @abs }}', {}, '17'
		yield '{{ 4 | @abs }}', {}, '4'
		yield '{{ "-19.86" | @abs }}', {}, '19.86'
		yield '{{ "/my/fancy/url" | @append: ".html" }}', {}, '/my/fancy/url.html'
		yield '{% assign filename = "/index.html" %}{{ "website.com" | @append: filename }}', {}, 'website.com/index.html'
		yield '{{ "adam!" | @capitalize | @prepend: "Hello " }}', {}, 'Hello Adam!'
		yield '{{ 4 | @at_least: 5 }}', {}, '4'
		yield '{{ 4 | @at_least: 3 }}', {}, '3'
		yield '{{ 4 | @at_most: 5 }}', {}, '5'
		yield '{{ 4 | @at_most: 3 }}', {}, '4'
		yield '{{ "title" | @capitalize }}', {}, 'Title'
		yield '{{ "my great title" | @capitalize }}', {}, 'My great title'
		yield '''{% assign site_categories = site.pages | @map: 'category' %}

{% for category in site_categories %}
  {{ category }}
{% endfor %}''', {'site': testly.Box(pages = [
	testly.Box(category = 'business'), 
	testly.Box(category = 'celebrities'), 
	testly.Box(category = ''), 
	testly.Box(category = 'lifestyle'), 
	testly.Box(category = 'sports'), 
	testly.Box(category = ''), 
	testly.Box(category = 'technology')
])}, '''
  business
  celebrities
  
  lifestyle
  sports
  
  technology
'''
		yield '''{% assign site_categories = site.pages | @map: 'category' | @compact %}

{% for category in site_categories %}
  {{ category }}
{% endfor %}''', {'site': testly.Box(pages = [
	testly.Box(category = 'business'), 
	testly.Box(category = 'celebrities'), 
	testly.Box(category = ''), 
	testly.Box(category = 'lifestyle'), 
	testly.Box(category = 'sports'), 
	testly.Box(category = ''), 
	testly.Box(category = 'technology')
])}, '''
  business
  celebrities
  lifestyle
  sports
  technology
'''
		yield '''{% assign fruits = "apples, oranges, peaches" | @split: ", " %}
{% assign vegetables = "carrots, turnips, potatoes" | @split: ", " %}

{% assign everything = fruits | @concat: vegetables %}
{% for item in everything %}
- {{ item }}
{% endfor %}''', {}, '''
- apples
- oranges
- peaches
- carrots
- turnips
- potatoes
'''
		yield '''{% assign furniture = "chairs, tables, shelves" | @split: ", " %}

{% assign everything = fruits | @concat: vegetables | @concat: furniture %}
{% for item in everything %}
- {{ item }}
{% endfor %}''', {'fruits': "apples, oranges, peaches".split(", "), 'vegetables': "carrots, turnips, potatoes".split(', ')}, '''
- apples
- oranges
- peaches
- carrots
- turnips
- potatoes
- chairs
- tables
- shelves
'''

		yield '{{ article.published_at | @date: "%a, %b %d, %y", "%m/%d/%Y" }}', {'article': testly.Box(published_at = '07/17/2015')}, 'Fri, Jul 17, 15'
		yield '{{ article.published_at | @date: "%Y", "%m/%d/%Y" }}', {'article': testly.Box(published_at = '07/17/2015')}, '2015'
		yield '{{ "March 14, 2016" | @date: "%b %d, %y", "%B %d, %Y" }}', {}, 'Mar 14, 16'
		yield 'This page was last updated at {{ "now" | @date: "%Y-%m-%d %H:%M" }}.', {}, 'This page was last updated at {}.'.format(__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M"))

		yield '{{ product_price | @default: 2.99 }}', {'product_price': None}, '2.99'
		yield '{{ product_price | @default: 2.99 }}', {'product_price': 4.99}, '4.99'
		yield '{{ product_price | @default: 2.99 }}', {'product_price': ''}, '2.99'

		yield '{{ 16 | @divided_by: 4 | int }}', {}, '4'  # 'python 3 returns 4.0 anyway'
		yield '{{ 5 | @divided_by: 3 | int }}', {}, '1'
		yield '{{ 20 | @divided_by: 7 | int }}', {}, '2'
		yield '{{ 20 | @divided_by: 7.0 | str | [:5] }}', {}, '2.857'

		yield '{{ "Parker Moore" | @downcase }}', {}, 'parker moore'
		yield '{{ "apple" | @downcase }}', {}, 'apple'

		yield '''{{ "Have you read 'James & the Giant Peach'?" | @escape }}''', {}, 'Have you read \'James &amp; the Giant Peach\'?'
		yield '{{ "Tetsuro Takara" | @escape }}', {}, 'Tetsuro Takara'

		yield '{{ 1.2 | @floor | int }}', {}, '1' # '1.0' in python
		yield '{{ 2.0 | @floor | int }}', {}, '2'
		yield '{{ 183.357 | @floor | int }}', {}, '183'
		yield '{{ "3.5" | @floor | int }}', {}, '3'

		yield '''{% assign beatles = "John, Paul, George, Ringo" | @split: ", " %}

{{ beatles | @join: " and " }}''', {}, '''
John and Paul and George and Ringo'''

		yield '{{ "          So much room for activities!          " | @lstrip }}', {}, "So much room for activities!          "
		
		yield '{{ 4 | @minus: 2 }}', {}, '2'
		yield '{{ 16 | @minus: 4 }}', {}, '12'
		yield '{{ 183.357 | @minus: 12 }}', {}, '171.357'
		yield '{{ 3 | @modulo: 2 }}', {}, '1'
		yield '{{ 24 | @modulo: 7 }}', {}, '3'
		yield '{{ 183.357 | @modulo: 12 }}', {}, '3.357'
		yield '{{ 4 | @plus: 2 }}', {}, '6'
		yield '{{ 16 | @plus: 4 }}', {}, '20'
		yield '{{ 183.357 | @plus: 12 }}', {}, '195.357'

		# 79
		yield '''
{% capture string_with_newlines %}
Hello
there
{% endcapture %}
{{ string_with_newlines | @newline_to_br }}''', {}, '''
Hello<br />there<br />'''

		yield '{{ "apples, oranges, and bananas" | @prepend: "Some fruit: " }}', {}, 'Some fruit: apples, oranges, and bananas'
		yield '''{% assign url = "liquidmarkup.com" %}

{{ "/index.html" | @prepend: url }}''', {}, '''
liquidmarkup.com/index.html'''

		yield '{{ "I strained to see the train through the rain" | @remove: "rain" }}', {}, 'I sted to see the t through the '
		# 83
		yield '{{ "I strained to see the train through the rain" | @remove_first: "rain" }}', {}, 'I sted to see the train through the rain'

		yield '{{ "Take my protein pills and put my helmet on" | @replace: "my", "your" }}', {}, 'Take your protein pills and put your helmet on'
		yield '{{ "Take my protein pills and put my helmet on" | @replace_first: "my", "your" }}', {}, 'Take your protein pills and put my helmet on'

		yield '''
{% assign my_array = "apples, oranges, peaches, plums" | @split: ", " %}

{{ my_array | @reverse | @join: ", " }}''', {}, '''

plums, peaches, oranges, apples'''

		yield '{{ "Ground control to Major Tom." | @split: "" | @reverse | @join: "" }}', {}, '.moT rojaM ot lortnoc dnuorG'

		yield '{{ 1.2 | @round }}', {}, '1.0'
		yield '{{ 2.7 | @round }}', {}, '3.0'
		#90
		yield '{{ 183.357 | @round }}', {}, '183.0'

		yield '{{ "          So much room for activities!          " | @rstrip }}', {}, '          So much room for activities!'
		yield '{{ "          So much room for activities!          " | @strip }}', {}, 'So much room for activities!'

		yield '{{ "Ground control to Major Tom." | @size }}', {}, '28'
		yield '{% assign my_array = "apples, oranges, peaches, plums" | @split: ", " %}{{ my_array | @size }}', {}, '4'

		yield '{{ "Liquid" | @slice: 0 }}', {}, 'L'
		yield '{{ "Liquid" | @slice: 2 }}', {}, 'q'
		# 97
		yield '{{ "Liquid" | @slice: 2, 5 }}', {}, 'quid'
		yield '{{ "Liquid" | @slice: -3, 2 }}', {}, 'ui'

		yield '{% assign my_array = "zebra, octopus, giraffe, Sally Snake" | @split: ", " %}{{ my_array | @sort | @join: ", " }}', {}, 'Sally Snake, giraffe, octopus, zebra'

		yield '''{% assign beatles = "John, Paul, George, Ringo" | @split: ", " %}

{% for member in beatles %}
  {{ member }}
{% endfor %}''', {}, '''
  John
  Paul
  George
  Ringo
'''
		yield '{{ "Have <em>you</em> read <strong>Ulysses</strong>?" | @strip_html }}', {}, 'Have you read Ulysses?'
		#102
		yield '''{% capture string_with_newlines %}
Hello
there
{% endcapture %}
{{ string_with_newlines | @strip_newlines }}''', {}, 'Hellothere',

		yield '{{ 3 | @times: 2 }}', {}, '6'
		yield '{{ 24 | @times: 7 }}', {}, '168'
		yield '{{ 183.357 | @times: 12 }}', {}, '2200.284'

		yield '{{ "Ground control to Major Tom." | @truncate: 20 }}', {}, 'Ground control to...'
		# 107
		yield '{{ "Ground control to Major Tom." | @truncate: 25, ", and so on" }}', {}, 'Ground control, and so on'
		yield '{{ "Ground control to Major Tom." | @truncate: 20, "" }}', {}, 'Ground control to Ma'

		yield '{{ "Ground control to Major Tom." | @truncatewords: 3 }}', {}, 'Ground control to...'
		yield '{{ "Ground control to Major Tom." | @truncatewords: 3, "--" }}', {}, 'Ground control to--'
		yield '{{ "Ground control to Major Tom." | @truncatewords: 3, "" }}', {}, 'Ground control to'

		yield '''{% assign my_array = "ants, bugs, bees, bugs, ants" | @split: ", " %}
{{ my_array | @uniq | @sort | @join: ", " }}''', {}, 'ants, bees, bugs'

		yield '{{ "Parker Moore" | @upcase }}', {}, 'PARKER MOORE'
		yield '{{ "APPLE" | @upcase }}', {}, 'APPLE'
		# 115
		yield '{{ "%27Stop%21%27+said+Fred" | @url_decode }}', {}, "'Stop!'+said+Fred"
		yield '{{ "john@liquid.com" | @url_encode }}', {}, 'john%40liquid.com'
		yield '{{ "Tetsuro Takara" | @url_encode }}', {}, 'Tetsuro+Takara'




	def testRender(self, text, data, out):
		l = Liquid(text)
		self.assertEqual(l.render(**data), out)

if __name__ == '__main__':
	testly.main(verbosity = 2)