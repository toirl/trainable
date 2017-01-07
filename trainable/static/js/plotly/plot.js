function initPlot(element, data) {
    var gd = document.getElementById(element);
    var resizeDebounce = null;

    for (i=0; i<data.length; i++) {
        figure.data[i].x = data[i][0];
        figure.data[i].y = data[i][1];
    }
    Plotly.plot(gd, figure.data, figure.layout, {displayModeBar: false});
}

function resizePlot() {
    var bb = gd.getBoundingClientRect();
    Plotly.relayout(gd, {
        width: bb.width,
        height: bb.height
    });
}

window.addEventListener('resize', function() {
    var gd = document.getElementById(element);
    var resizeDebounce = null;
    if (resizeDebounce) {
        window.clearTimeout(resizeDebounce);
    }
    resizeDebounce = window.setTimeout(resizePlot, 100);
});
