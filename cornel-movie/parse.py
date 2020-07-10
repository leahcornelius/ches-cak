import pandas as pd
import pickledb
db = pickledb.load('cornell_lines_out.db', False)
import json
df = pd.read_csv('./movie_lines.txt', sep = '\+\+\+\$\+\+\+',
                 engine = 'python', index_col = False)
df.head()
df.drop(df.columns[1:4], axis=1, inplace=True)
for value in df.values.tolist():
  db.set(str(value[0]).strip(), str(value[1]).strip())
  print("Set key: ", str(value[0]).strip(),
        ", to value: ", str(value[1]).strip())

df = pd.read_csv('./movie_conversations.txt',
                 sep='\+\+\+\$\+\+\+', engine='python', index_col=False)
df.head()
df.drop(df.columns[1:3], axis=1, inplace=True)
f = open("../datasets/conell_movie_out.yml", "a")
f.write("---\n")
f.write("categories:\n") 
f.write("  - cornell_movie\n")
f.write("conversations:\n")
for value in df.values.tolist():
    alpha = True
    as_json ='{"val": ' + value[1].replace("'", '"') + '}'
    conv = json.loads(as_json)['val']
    for line_code in conv:      
      line = db.get(line_code)
      print(line)
      if line == False:
        line = ""
      line = line.replace('"', "'")
       # line.replace("'", "")
      if alpha:
        f.write('- - "' + str(line).strip() + '"\n')
        alpha = False
      else:
        f.write('  - "' + str(line).strip() + '"\n')
