function saveLevel(root) {
    var retObj = {};
    console.log("root is:", root);
    root.$children.forEach((elem, ndx, arr) => {
        if (elem.$children.length > 0 && elem.recursiveSave) {
            //This element has children we need to ge the values of that
            retObj[elem.block] = saveLevel(elem);
        }
        else {
            retObj[elem.block] = elem.getAllData();
        }
    });

    return retObj;
}

export default saveLevel;