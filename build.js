const CSS_FILE_ORDER = [
// -------------- FILE NAME ------------ PURPOSE --------------
        'etc.css',            // body, buttons, and wiki
        'header.css',         // subreddit header
        'submit.css',         // submit form

        'linklisting.css',    // styles for the link listing page
        'thing.css',          // styles for thing elements (links and comments alike)
        'tagline.css',        // thing tagline
        'linkflair.css',      // link flair, link flair filters, and link flair selector
        'link-pinnable.css',  // pinnable link for video posts

        'commentfix.css',     // styles for specifically comments
        'commentpage.css',    // styles for the comment page menus, usertext editor, etc.
        'usertext.css',       // styles for usertext editor, area, and markdown

        'sidecommon.css',     // sidebar common header and checkboxes
        'sidebar.css',        // sidebar
        'sidemd.css',         // sidebar md
        'sidecontentbox.css',  // sidecontentbox

        'announce.css',       // announcements modules and bar

        'search.css',         // search page (does not include search input in sidebar)
        'footer.css',         // subreddit footer
        'modpages.css',       // any moderator pages that required additional CSS

        'flair.css',          // user flairs
        'userflair.css',      // user flairs
        'flairbg.css',        // user flairs
        'moontheme.css',      // night mode
        'banner.css',         // banner
        'misc.css'            // miscellaneous

        // add-ons
        // -------
        // 'sm_release.css',     // fancy CSS for Pokemon Sun & Moon Release Megathread
        // 'magikarp.css',       // Magikarp Week Banner CSS
        // 'direct_banner.css',  // Direct Banner (temp add-on)
];

const fs = require('fs');
const CleanCSS = require('clean-css');

const writeOutputFile = (filepath, contents, success, failure) => {
    fs.truncate(filepath, 0, () => {
        fs.writeFile(filepath, contents, 'utf8', (err) => {
            if (err) {
                if (failure) failure("Failed to write output file (" + filepath + ") " + err);
            } else {
                if (success) success();
            }
        });
    });
};

function packOutput(files) {
    let styles = '';

    files.forEach((f) => {
        styles += fs.readFileSync(f, "utf8");
    });

    return styles;
}

function minify(styles, build_ver) {
    var out = {
        stats: { originalSize: 0, minifiedSize: 0 },
        styles: '',
    };

    let res = new CleanCSS({
        level: 2,
    }).minify(styles)

    if (res.errors.length)
        reject(output.errors);
    else if (res.warnings.length)
        reject(output.warnings);

    out.styles = '/*!\n' +
        ' * CSS theme for /r/Pokemon; build #' + (build_ver) + '\n' +
        ' * Authors: Hero_of_Legend, technophonix1, Atooz, kwwxis, & Haruka-sama' + '\n' +
        ' */\n' + res.styles;
    out.stats.originalSize = res.stats.originalSize;
    out.stats.minifiedSize = res.stats.minifiedSize;
    return out;
}

function get_build_ver() {
    return parseInt(fs.readFileSync("./build.dat", "utf8"));
}

(function() {
    let build_ver = get_build_ver();
    console.log('\nBUILD #' + build_ver)
    console.log('Minifying...');

    new Promise((resolve, reject) => {
        let names = {
            src_dir: 'src/',
            dist_dir: './',
            dist_file: 'dist.css',
            umin_file: 'unmin.css',
        };

        let uminified = packOutput(CSS_FILE_ORDER.map(f => names.src_dir+f));
        let res = minify(uminified, build_ver);

        console.log('Original size: ' + res.stats.originalSize + ' bytes');
        console.log('Minified size: ' + res.stats.minifiedSize + ' bytes');

        writeOutputFile(names.dist_dir + names.umin_file, uminified, resolve, reject);
        writeOutputFile(names.dist_dir + names.dist_file, res.styles, resolve, reject);
        writeOutputFile("./build.dat", ""+(build_ver+1), resolve, reject);
    }).then(
        () => console.log('Done!'),
        (reason) => console.log(reason)
    );
})();