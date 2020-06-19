## The code adheres to the PEP 8 style guide and follows common best practices, including:

Variable and function names are clear.
Endpoints are logically named.
Code is commented appropriately.
The README file includes detailed instructions for scripts to install any project dependencies, and to run the development server.
Secrets are stored as environment variables.
Code comments and organization
:white_check_mark: No problems found regarding the comments, variable names, and code organization.

Pep8/pycodestyle report
:x: Running the `pycodestyle` tool (which is the new name to pep-8) gives some warnings, review them and apply the changes

:warning: It is important to follow code patterns because it helps to create a standard between codebases, improving collaboration and common understanding

PS: Here is a link that may help you to fix the long line warnings

PS2: Here is a post that may help you better understand why using raw except is not a good practice.

PS E:\downloads\Project_3_Coffee_shop_full_stack_-_submit\backend\src> pycodestyle api.py
api.py:19:1: E265 block comment should start with '# '
api.py:21:1: E266 too many leading '#' for block comment
api.py:27:80: E501 line too long (107 > 79 characters)
api.py:33:13: E225 missing whitespace around operator
api.py:39:5: E722 do not use bare 'except'
api.py:42:1: E305 expected 2 blank lines after class or function definition, found 1
api.py:47:80: E501 line too long (107 > 79 characters)
api.py:61:5: E722 do not use bare 'except'
api.py:63:1: E305 expected 2 blank lines after class or function definition, found 0
api.py:69:80: E501 line too long (132 > 79 characters)
api.py:79:15: E225 missing whitespace around operator
api.py:83:14: E225 missing whitespace around operator
api.py:89:5: E722 do not use bare 'except'
api.py:90:7: E111 indentation is not a multiple of four
api.py:91:1: E305 expected 2 blank lines after class or function definition, found 0
api.py:99:80: E501 line too long (126 > 79 characters)
api.py:121:5: E722 do not use bare 'except'
api.py:123:1: E305 expected 2 blank lines after class or function definition, found 0
api.py:130:80: E501 line too long (109 > 79 characters)
api.py:139:9: W291 trailing whitespace
api.py:146:5: E722 do not use bare 'except'
api.py:149:1: E266 too many leading '#' for block comment
api.py:150:1: E305 expected 2 blank lines after class or function definition, found 1
api.py:156:38: W291 trailing whitespace
api.py:161:1: E305 expected 2 blank lines after class or function definition, found 1
api.py:165:38: W291 trailing whitespace
api.py:174:55: W291 trailing whitespace
api.py:184:1: E305 expected 2 blank lines after class or function definition, found 1
api.py:186:55: W291 trailing whitespace
api.py:203:12: W292 no newline at end of file


## Suggestion

Enabling CORS is important but must be done carefully. Keep in mind that security issues can arise from this.

Take a look at this updated guide of best practices and things to look out while implementing CORS. https://www.pivotpointsecurity.com/blog/cross-origin-resource-sharing-security/

You can explore a little bit further the code documentation opportunity here. Flask API's has great integrations with the Swagger tool, but you do not need to go fancy on this one, just documenting the entry parameters and expected return would be great enough.

Check out this thread, https://stackoverflow.com/questions/43911510/how-to-write-docstring-for-url-parameters, which contains a ton of great tips and examples on how to enable your documentation to be read by swagger, and by the humans too!

Great job adding some Python docstrings which provide an entry-level of the application documentation; it is helpful to remember you in the future or even bring other developers to contribute to your source code.
