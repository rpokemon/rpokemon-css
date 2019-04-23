const CSS_FILE_ORDER = [
/// FILE NAME ------------------// PURPOSE ---------------------------------------------------------

    // *********************************************************************************************
    // header and footer
    'etc.css',                  // miscellaneous (at start)
    'header.css',               // subreddit header
    'footer.css',               // subreddit footer

    // *********************************************************************************************
    // things, listings, and usertext

    'linklisting.css',          // styles for the link listing page
    'thing.css',                // styles for thing elements (links and comments alike)
    'tagline.css',              // thing tagline
    'linkflair.css',            // link flair, link flair filters, and link flair selector
    'link-pinnable.css',        // pinnable link for video posts
    'commentfix.css',           // styles for specifically comments
    'commentpage.css',          // styles for the comment page menus, usertext editor, etc.
    'usertext.css',             // styles for usertext editor, area, and markdown

    // *********************************************************************************************
    // sidebar

    'sidecommon.css',           // sidebar common header and checkboxes
    'sidebar.css',              // sidebar
    'sidemd.css',               // sidebar md
    'sidecontentbox.css',       // sidecontentbox

    // *********************************************************************************************
    // Other pages
    'submit.css',               // submit form
    'search.css',               // search page (does not include search input in sidebar)
    'modpages.css',             // any moderator pages that required additional CSS

    // *********************************************************************************************
    // flairs

    'flair.css',                // flair sheets
    'userflair.css',            // user flairs
    'ballflair.css',            // ball flairs
    'nameplate.css',            // author nameplates

    // *********************************************************************************************
    // Other modules
    'announce.css',             // announcements modules and bar (must come after header & sidebar)
    'banner.css',               // banner (must come after header.css to override)
    'nightmode-misc.css',       // night mode

    // *********************************************************************************************
    // add-ons for specific events

    // 'sm_release.css',        // fancy CSS for Pokemon Sun & Moon Release Megathread
    // 'magikarp.css',          // Magikarp Week Banner CSS
    // 'direct_banner.css',     // Direct Banner (temp add-on)
];


(function(readFile, writeFile) {
    console.log('Minifying...');

    const CleanCSS = require('clean-css');
    const p = CSS_FILE_ORDER.map(f => readFile('src/'+f));

    Promise.all(p).then(stylesheets => {
        const unminified = stylesheets.join('');
        const res = new CleanCSS({ level: 2 }).minify(unminified);

        if (res.errors.length) throw res.errors;
        if (res.warnings.length) throw res.warnings;

        Promise.all([
            writeFile('./unmin.css', unminified),
            writeFile('./dist.css', res.styles),
        ]).then(
            () => {
                console.log(`Original size: ${res.stats.originalSize} bytes`);
                console.log(`Minified size: ${res.stats.minifiedSize} bytes`);
                console.log('Done!');
            },
            (reason) => console.log(reason)
        );
    }).catch(reason => console.log(reason));
})(
    function(filepath) {
        return new Promise((resolve, reject) => {
            require('fs').readFile(filepath, 'utf8', (err,data) => {
                if (err) reject(`Failed to read source file (${filepath}) ${err}`);
                else resolve(data.toString());
            });
        });
    },
    function(filepath, contents) {
        return new Promise((resolve, reject) => {
            require('fs').writeFile(filepath, contents, { encoding:'utf8', flag:'w' }, (err) => {
                if (err) reject(`Failed to write output file (${filepath}) ${err}`);
                else resolve();
            });
        });
    },
);