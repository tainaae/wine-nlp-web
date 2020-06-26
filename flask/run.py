from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__, template_folder='templates')

#caso app seja chamado 
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/suggestion', methods=['POST'])
def getChecked():
    data = request.get_json()
    print (data)
    
    from userdata_to_matched_dict import create_nlp_string
    string = create_nlp_string(data)
    print (string)
    #return string
    #num_cluster = 3 #

    proc = subprocess.Popen(["python3", "recommendation.py", "'{}'".format(string)], stdout=subprocess.PIPE)
    output = proc.stdout.read()
    num_cluster = int(output.decode('UTF-8'))
    print(num_cluster)

    #return num_cluster
    from lib.get_datacluster import get_top4
    top4_df = get_top4(num_cluster)
    top4_country = top4_df['country'].values.tolist()
    top4_variety = top4_df['variety'].values.tolist()
    top4_points = top4_df['points'].values.tolist()
    
    top4_all_in_object = [{'country':country, 'variety': variety, 'points': points} for country, variety, points in zip(top4_country, top4_variety, top4_points)]
    print (top4_all_in_object)
#    print (JSONP_top4_country)
#    return JSONP_top4_country, JSONP_top4_variety,JSONP_top4_points
    return jsonify (top4_all_in_object)

if __name__ == '__main__':
        
    app.run(debug = True)


