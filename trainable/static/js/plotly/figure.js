var figure = {
    "frames": [], 
    "layout": {
        "autosize": false, 
        "showlegend": true, 
        "margin": {t:0},
        "breakpoints": [], 
        "barmode": "group", 
        "bargap": 0.47, 
        "bargroupgap": 0,
        "yaxis": {
            "autorange": true, 
            "type": "linear", 
            "domain": [
                0,
                0.45
            ], 
            "title": "Duration [min]"
        }, 
        "yaxis2": {
            "domain": [
                0.55, 
                1
            ], 
            "title": "Intesity [xxx]", 
            "anchor": "x", 
            "type": "linear", 
            "autorange": true
        }, 
        "xaxis": {
            "autorange": true, 
            "domain": [
                0, 
                1
            ], 
            "title": "Week"
        } 
    }, 
    "data": [
        {
            "name": "Planned Duration", 
            "mode": "markers", 
            "y": [
            ], 
            "x": [
            ], 
            "autobiny": true, 
            "type": "bar", 
            "orientation": "v"
        }, 
        {
            "name": "Achieved Duration", 
            "marker": {
                "color": "rgb(115, 198, 255)"
            }, 
            "y": [
            ], 
            "x": [
            ], 
            "autobiny": true, 
            "type": "bar", 
            "orientation": "v"
        }, 
        {
            "autobinx": true, 
            "yaxis": "y2", 
            "name": "Planned Intensity", 
            "xaxis": "x", 
            "y": [
            ], 
            "x": [
            ], 
            "type": "bar", 
            "autobiny": true
        }, 
        {
            "autobinx": true, 
            "yaxis": "y2", 
            "name": "Achived Intensity", 
            "marker": {
                "color": "rgb(137, 240, 137)"
            }, 
            "xaxis": "x", 
            "y": [
            ], 
            "x": [
            ], 
            "type": "bar", 
            "autobiny": true
        }
    ]
};

var fitnessFigure = {
    "frames": [], 
    "layout": {
        "autosize": true, 
        "yaxis": {
            "type": "linear", 
            "autorange": true, 
            "title": "Form"
        }, 
        "plot_bgcolor": "rgb(255, 255, 255)",  
        "showlegend": true, 
        "margin": {t:0},
        "breakpoints": [], 
        "yaxis2": {
            "title": "TSS", 
            "overlaying": "y", 
            "anchor": "x", 
            "type": "linear", 
            "autorange": true, 
            "side": "right"
        }, 
        "xaxis": { 
            "title": "Day"
        }, 
        "hovermode": "closest"
    }, 
    "data": [
        {
            "yaxis": "y2", 
            "name": "TSS", 
            "marker": {
                "color": "rgb(214, 39, 40)", 
                "sizeref": 3.5
            }, 
            "mode": "markers", 
            "type": "scatter", 
            "autobiny": true
        }, 
        { 
            "name": "CTL",  
            "mode": "lines", 
            "fillcolor": "rgb(223, 223, 223)", 
            "line": {
                "color": "rgb(68, 68, 68)"
            }, 
            "fill": "tozeroy", 
            "type": "scatter"
        }, 
        { 
            "name": "ATL", 
            "mode": "lines", 
            "line": {
                "color": "rgb(255, 127, 14)"
            }, 
            "type": "scatter", 
            "autobiny": true
        }, 
        { 
            "name": "TSB", 
            "mode": "lines", 
            "line": {
                "color": "rgb(188, 189, 34)"
            }, 
            "type": "scatter", 
            "autobiny": true
        }
    ]
}
