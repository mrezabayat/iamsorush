let gulp     = require("gulp");
let request  = require("request");
let gravatar = require('gravatar');
let fs       = require('fs');

var buildDest = "build";

gulp.task("build:comments", function (done) {

    if (process.env.NETLIFY_APPROVED_COMMENTS_FORM_ID === undefined) {
        console.log("Missing NETLIFY_APPROVED_COMMENTS_FORM_ID environment variable!");
        done();
        return;
    }

    if (process.env.NETLIFY_API_AUTH === undefined) {
        console.log("Missing NETLIFY_API_AUTH environment variable!");
        done();
        return;
    }

    let commentsUrl = `https://api.netlify.com/api/v1/forms/${process.env.NETLIFY_APPROVED_COMMENTS_FORM_ID}/submissions/?access_token=${process.env.NETLIFY_API_AUTH}`;

    request(commentsUrl, function(err, response, body) {

        if (!err && response.statusCode === 200) {

            let comments = {};

            for (let item of JSON.parse(body)) {

                let comment = {
                    first_name: item.data.first_name,
                    last_name: item.data.last_name,
                    gravatar: gravatar.url(item.data.email),
                    comment: item.data.comment.trim(),
                    received: item.data.received
                };

                // Add it to an existing array or create a new one
                if (comments[item.data.path]){
                    comments[item.data.path].push(comment);
                }
                else {
                    comments[item.data.path] = [comment];
                }
            }

            // write data to file
            fs.mkdir(buildDest, function(err) {
                if (err && err.code !== "EEXIST") {
                    console.log(err);
                    done();
                }
                else {
                    fs.mkdir(buildDest + "/data", function(err) {
                        if (err && err.code !== "EEXIST") {
                            console.log(err);
                            done();
                        }
                        else {
                            fs.writeFile(buildDest + "/data/comments.json", JSON.stringify(comments, null, 2), function(err) {
                                if (err) {
                                    console.log(err);
                                }
                                else {
                                    console.log("Comments data saved.");
                                }
                                done();
                            });
                        }
                    });
                }
            });
        }
        else {
            console.log("Couldn't get comments from Netlify");
            done();
        }
    });
});
