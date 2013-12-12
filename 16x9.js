var mods = [16, 8, 4, 2];

for (var j in mods) {
    console.log("mod " + mods[j] + " ");

    for (var i = 1; i < 600; i++) {
        var h = i * mods[j];
        if ((h % 9) === 0) {
            console.log(h * 16 / 9 + "x" + h + " ");
        }
    }
}
