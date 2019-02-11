var fileList;
var fileIndex;
var imgDir = "./targets"
var zoomlevel = "600";

macro "Initalise mask process [a]" {
    var fileList = getFileList(imgDir)
    var fileIndex = 0;
}

macro "Do debug [w]" {
    print(fileList[fileIndex]);
}

macro "Do next mask [z]" {
    filename = fileList[fileIndex];
    open(imgDir + "/" + filename);
    run("Set... ", "zoom=" + zoomlevel); 
    // run("In [+]");
}

macro "Skip to next [e]" {
    fileIndex = fileIndex + 1
}

macro "Save mask [q]" {
    outputFile = replace(fileList[fileIndex], ".png", ".bmp");
    run("Create Mask");
    saveAs("BMP", imgDir + "/masks/" + outputFile);
    selectWindow(outputFile);
    close();
    selectWindow(fileList[fileIndex]);
    close();
    fileIndex = fileIndex + 1;
}
