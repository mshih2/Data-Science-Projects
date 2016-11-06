module.exports = stringify;

function stringify(obj, ignoreFunc, printFuncContent, former, depth, path) {
    var indent = "    ";
    if (ignoreFunc == undefined) {
        ignoreFunc = false;
    }
    if (printFuncContent == undefined) {
        printFuncContent = false;
    }
    if (former == undefined) {
        former = "";
    }
    if (depth == undefined) {
        depth = 0;
    }
    if (path == undefined) {
        path = [];
    }

    var prefix = "" + new Array(depth + 1).join(indent);
    var encountered = (path.indexOf(obj) !== -1);
    path.push(obj);

    var result = former;
    if (isList(obj)) {
        if (!encountered) {
            if(obj.length > 0) {
                result += "[\n";
                for (var i = 0; i < obj.length; i++) {
                    result += indent + prefix + i + ": ";
                    result += stringify(obj[i], ignoreFunc, printFuncContent, "", depth + 1, [].concat(path));
                    if (i < obj.length - 1) {
                        result += ",\n";
                    } else {
                        result += "\n";
                    }
                }
                result += prefix + "]";
            } else {
                result += "[ ]";
            }
        } else {
            result += "[Circular]";
        }
    } else if (isMapping(obj)) {
        if (!encountered) {
            var count = 0;
            var totalCount = 0;
            for (var key in obj) {
                totalCount++;
                if (!isFunction(obj[key]) || !ignoreFunc) {
                    count++;
                }
            }
            if(totalCount > 0) {
                result += "{\n";
                var counter = 0;
                for (var key in obj) {
                    var value = obj[key];
                    if (!isFunction(value) || !ignoreFunc) {
                        counter++;
                        result += prefix + indent + key + ": " + stringify(value, ignoreFunc, printFuncContent, "", depth + 1, [].concat(path));
                        if (counter < count) {
                            result += ",\n";
                        } else {
                            result += "\n";
                        }
                    }
                }
                result += prefix + "}"
            } else {
                result += "{}";
            }

        } else {
            result += "[Circular]"
        }
    } else if (isFunction(obj)) {
        if (printFuncContent) {
            var lines = ("" + obj).split("\n");
            var funcContent = "";
            var lastLine = lines[lines.length - 1];
            var lasIndent = lastLine.replace(lastLine.trim(), "")
            for(var i = 0; i < lines.length; i++) {
                if (i === 0) {
                    funcContent += lines[i];
                } else {
                    funcContent += prefix + lines[i].substring(lasIndent.length, lines[i].length);
                }
                if (i !== lines.length - 1) {
                    funcContent += "\n";
                }
            }
            result += funcContent;
        } else {
            result += "_function_";
        }
    } else {
        result += obj + "";
    }
    return result;
}



function isList(obj) {
    return (Object.prototype.toString.call(obj) === '[object Array]' || Object.prototype.toString.call(obj) === '[object Arguments]') && Object.keys(obj).every(function(e) {
            return !isNaN(parseInt(e));
        });
}

function isMapping(obj) {
    return Object.prototype.toString.call(obj) === '[object Object]' || ((Object.prototype.toString.call(obj) === '[object Array]' || Object.prototype.toString.call(obj) === '[object Arguments]') && Object.keys(obj).some(function(e) {
            return isNaN(parseInt(e));
        }));
}

function isFunction(obj) {
    return Object.prototype.toString.call(obj) === '[object Function]';
}







