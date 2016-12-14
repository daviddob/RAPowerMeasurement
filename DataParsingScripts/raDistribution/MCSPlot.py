import sys
import plotly.plotly as py
import plotly.graph_objs as go
import json
from pprint import pprint

def main(argv):
    results = json.loads(open("I:\\data\\CSE630\\Results\\ra_mcs.json", "r").read())    
    for bandwidth in results:
        for location in results[bandwidth]:
            mcsindex=0
            xlist = []
            ylist = []
            for mcsfreq in results[bandwidth][location]:
                xlist.append(mcsindex)
                ylist.append(mcsfreq)
                mcsindex += 1
            print(xlist)
            print(ylist)
            data = [go.Bar(x=xlist,y=ylist)]
            name=bandwidth+location
            layout = go.Layout(
                title=name,
                xaxis=dict(title='MCS Index'),
                yaxis=dict(title='Frequency')
            )
            figure = go.Figure(data=data, layout=layout)
            #py.plot(figure, filename=name)
                
if __name__ == "__main__":
    main(sys.argv[1:])
