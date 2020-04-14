import pandas as pd

links = ['https://m.facebook.com/groups/470640109647012/?ref=group_browse'
,'https://m.facebook.com/groups/213136165450471/?ref=group_browse'
,'https://m.facebook.com/groups/1626192214309398/?ref=group_browse']

output_html = '<html>\n<body>\n\t<script async defer src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v3.2"></script>\n'
for i in range(len(links)):
    link = str(links[i])
    output_html += '\t<div class="fb-post" data-href="%s" data-width="500"></div>\n' % links[i]

output_html += '</body>\n</html>'

print(output_html)