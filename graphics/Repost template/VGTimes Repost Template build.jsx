// Builds "VGTimes Repost Template" natively in Photoshop (fallback if the PSD text layers do not open).
// Run: Photoshop > File > Scripts > Browse... Keep repost_avatar.png and repost_badge.png next to this file.
#target photoshop
(function () {
    var dir = File($.fileName).parent;
    app.preferences.rulerUnits = Units.PIXELS;
    app.preferences.typeUnits = TypeUnits.PIXELS;
    var doc = app.documents.add(1080, 1920, 72, "VGTimes Repost Template", NewDocumentMode.RGB, DocumentFill.WHITE);
    doc.activeLayer.name = "BG white";

    function rgb(r, g, b) { var c = new SolidColor(); c.rgb.red = r; c.rgb.green = g; c.rgb.blue = b; return c; }

    // video placeholder
    var v = doc.artLayers.add(); v.name = "VIDEO - replace (1080x760, y 610)";
    doc.selection.select([[0, 610], [1080, 610], [1080, 1370], [0, 1370]]);
    doc.selection.fill(rgb(28, 28, 30)); doc.selection.deselect();

    function place(fileName, x, y, name) {
        var f = File(dir + "/" + fileName);
        if (!f.exists) { alert("Not found: " + fileName); return; }
        var src = app.open(f); src.selection.selectAll(); src.selection.copy(); src.close(SaveOptions.DONOTSAVECHANGES);
        app.activeDocument = doc;
        var l = doc.paste(); l.name = name;
        var b = l.bounds; l.translate(x - b[0].as("px"), y - b[1].as("px"));
    }
    place("repost_avatar.png", 64, 256, "Avatar VGTimes");
    place("repost_badge.png", 464, 276, "Verified badge");

    function pointText(name, text, font, size, color, x, baseline) {
        var l = doc.artLayers.add(); l.kind = LayerKind.TEXT; l.name = name;
        var t = l.textItem; t.contents = text; t.font = font; t.size = size;
        t.color = color; t.antiAliasMethod = AntiAlias.SHARP; t.position = [x, baseline];
        return l;
    }
    pointText("VGTimes", "VGTimes", "Arial-BoldMT", 53, rgb(0, 0, 0), 209, 313);
    pointText("@VGTimes", "@VGTimes", "ArialMT", 36, rgb(83, 100, 113), 210, 364);

    var h = doc.artLayers.add(); h.kind = LayerKind.TEXT; h.name = "HEADLINE";
    var ht = h.textItem; ht.kind = TextType.PARAGRAPHTEXT;
    ht.position = [64, 399]; ht.width = 952; ht.height = 200;
    ht.contents = "MY FAVORITE CHILDHOOD RACING GAME GOT PORTED TO THE WEB — AND NOW 3,000 PLAYERS ARE FREE ROAMING TOGETHER!";
    ht.font = "Arial-Black"; ht.size = 43; ht.useAutoLeading = false; ht.leading = 47;
    ht.color = rgb(0, 0, 0); ht.antiAliasMethod = AntiAlias.SHARP;

    var out = File(dir + "/VGTimes Repost Template (built).psd");
    var o = new PhotoshopSaveOptions(); o.layers = true;
    doc.saveAs(out, o, false);
    alert("Saved: " + out.fsName);
})();
