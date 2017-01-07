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
}
