# Post2Ghost

This repository contains the Python3 CLI application **Post2Ghost** which allows to upload articles written in [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) to draft blog posts in [Ghost](https://ghost.org/). For this, the application is using the [Ghost v0.1 Public API](https://api.ghost.org/v0.1/docs). Additionally, tags can be maintained in Ghost using plain JSON dictionary files.

Post2Ghost allows for a [Git](https://git-scm.com/) centric workflow where articles are authored in Markdown files before being programmatically released to draft articles in Ghost.

This application is used by the authors of [How Hard Can It Be?!](https://www.how-hard-can-it.be) on a regular base.


## You Have

Before you can use Post2Ghost out of the box, you need
 - access to a Ghost installation with the [Ghost v0.1 Public API](https://api.ghost.org/v0.1/docs) enabled (available in up to and including [Ghost release 2.10.1](https://github.com/TryGhost/Ghost/releases/tag/2.10.1))
 - a user account on the Ghost installation
 - a recent version of [`Python3`](https://www.python.org/downloads/)
 - the `ghost-client` Python package available at https://pypi.org/project/ghost-client/

Moreover, you probably also have a blog post written in Markdown ready to be uploaded. 


## You Want

Using Post2Ghost allows you to
 - leverage the simplicity of distraction free writing using Markdown
 - use your favourite editor for writing articles in Markdown
 - stop the copy and past madness between your favourite editor and the Ghost Markdown editor
 - programmatically upload and update draft articles from the command line
 - build a Git centric workflow for articles


## Initial Setup

Unfortunately, Post2Ghost can't just magically guess all parameters required to access your Ghost installation. It needs your help on this. In more detail, it needs the following parameters:

1. The `base_url` of your Ghost installation. This is where Ghost is located. In the case of [How Hard Can It Be?!](https://www.how-hard-can-it.be), that's [https://www.how-hard-can-it.be](https://www.how-hard-can-it.be).
2. The `client_id` and `client_secret` of your Ghost installation. These two parameters can be found in the source code of any post (not the start page or the admin area) in your blog. Simply visit your Ghost installation, browse through the source code, and search for the two keywords.
3. The `username` and `password` that you use to access the admin area of your Ghost installation.

All of the above parameters need to be stored in your home directory at `~/.post2ghost/config.json`. This is a user wide setting by design so that Post2Ghost can be used regardless of the current directory.

In the case of [How Hard Can It Be?!](https://www.how-hard-can-it.be), the `~/.post2ghost/config.json` configuration file contains
```
{
  "base_url": "https://www.how-hard-can-it.be",
  "client_id": "ghost-frontend",
  "client_secret": "65ae2ad78214",
  "username": "<redacted>",
  "password": "<redacted>"
}
```

Here, `username` and `password` have been redacted for security reasons — these are the only two parameters that should actually be treated as secrets. The remaining information is already publicly available on the website.


## Blog Post Metadata

Post2Ghost allows to enrich a blog post written in Markdown with JSON metadata. Here, the _JSON metadata preceds the actual blog article in the same file_ and is used in [Ghost's publishing options](https://docs.ghost.org/faq/publishing-options/) to automatically populate fields like

- title for the blog post
- excerpt (this is the text alongside the article on the start page)
- feature image (the image that is being displayed for the article on the start page)
- slug (the URL used to reference the article)
- tags (logical folders that the article should be filed under)


At a _bare minimium_, `title` and `custom_excerpt` need to be defined as these values are propagated to the corresponding settings for
 - Search engines
 - Twitter cards and
 - Facebook cards

Here, the propagation can be overwritten by providing specific values. See the [official Ghost API documentation on posts](https://api.ghost.org/docs/post) for details.


### An Example

For the initial blog post [How Hard Can It Be?!](https://www.how-hard-can-it.be/how-hard-can-it-be/), the metadata is
```
{
    "title": "How Hard Can It Be?!",
    "feature_image": "images/how-hard-can-it-be.jpg",
    "custom_excerpt": "Time to give back to the community! Because technology should be simple.",
    "slug": "how-hard-can-it-be",
    "tags": ["How Hard Can It Be?!"]
}
```

Here, the `feature_image` is stored _locally_ at `images/how-hard-can-it-be.jpg`. Note that the path to the image is _relative_.

The `slug` is manually set to `how-hard-can-it-be` and the `tags` is set to the _existing_ tag `"How Hard Can It Be?!"`. See also the limitations around referencing tags as outlined below.


### A Note on Metadata Inside Markdown Articles

As described above, the _metadata has to precede the actual blog post inside the same file_.

This is a deliberate design decision in order to keep all information related to a blog post in one place. The only downside  is that the metadata has to be stored in valid JSON in order to be properly detected. Most likely, your editor will get confused by the mix of JSON and Markdown. In case of parsing errors, the upload will fail as the minimum required metadata parameters are missing. Simply go back, fix the JSON errors, and try again.


## Image Handling

Post2Ghost automatically detects and handles all images in a given Markdown file. For that, it replaces references to local files with references to images it has uploaded to the Ghost installation. In case the image has been uploaded by Post2Ghost before, a reference to the previously uploaded image is used. All comparisons are MD5 based and tracked in `~/.post2ghost/uploaded_images.json`.

Moreover, Post2Ghost detects links to external images and leaves them unchanged.


## A Minimum Starter Template

A minimum starter template is located at [templates/minimum-post.md](templates/minimum-post.md) and may look like

```
{
    "title": "Post2Ghost",
    "custom_excerpt": "This post was uploaded using Post2Ghost",
}


# Post2Ghost

This post and its metadata was uploaded using Post2Ghost.
```


## A Starter Template With More Options

A starter template that leverages an external `feature_image` from [Unsplash](https://unsplash.com/) alongside other options is located at [templates/post.md](templates/post.md) and contains

```
{
    "title": "Post2Ghost",
    "custom_excerpt": "This post was uploaded using Post2Ghost.",
    "feature_image": "https://images.unsplash.com/photo-1548474197-fe5543f71ceb?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&ixid=eyJhcHBfaWQiOjExNzczfQ",
    "slug": "post2ghost",
    "tags": ["Ghost", "Python"]
}


# Post2Ghost

This post and its metadata was uploaded using Post2Ghost.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
```


## Creating and Updating Draft Posts

After completing the initial setup described above, creating and updating a draft post follows the same process by design.

### Uploading and Article

An article in `/path/to/post.md` can be _uploaded_ via
```
python3 post2ghost.py -f /path/to/post.md
```
Note that all references to images _inside_ `/path/to/post.md` need to be relative to path `/path/to/`. In other words, if you preview your article, all images should show correctly.


### Updating an Article

Article `/path/to/post.md` can be _updated_ using the identical command, i.e.,
```
python3 post2ghost.py -f /path/to/post.md
```


### Publishing an Article

In order to publish article `/path/to/post.md`, please log into your Ghost installation, check that the article turned out the way you expected it to be and _manually_ hit the [**Publish** button](https://docs.ghost.org/faq/using-the-editor/) in Ghost.


## Managing Tags

Post2Ghost also allows to manage tags in a Ghost installation. Tags are JSON dictionaries as defined in the [official API documentation](https://api.ghost.org/docs/tag) that are stored inside individual files for easier versioning.


### A Minimum Tag Template

A minimum tag template is located at [templates/tag.json](templates/tag.json) and may look like

```
{
    "name": "Your Tag",
    "description": "Description of your tag.",
    "slug": "your-tag",
    "meta_title": "Your Tag",
    "meta_description": "Description of your tag."
}
```

### Execution

A tag in `/path/to/tag.json` can be uploaded and updated via
```
python3 update_tag.py -f /path/to/tag.json
```


## Known Limitations of Post2Ghost

The following is a list of known limitations when uploading articles.

- The metadata needs to be formatted in valid JSON as currently no JSON parsing errors are detected
- Tags can only be referred by name
- Only draft posts can be updated

Feel free to contribute towards eventually removing the above limitations. This is open source after all.


## FAQs

### Why is Post2Ghost Complaining About Missing Required Keys Even Though I've Supplied Them in the Metadata?!

There's a chance that your metadata JSON isn't actually valid. This will lead to Post2Ghost not being able to detect any metadata and hence complain about missing keys.

Usually, the solution is to fix the syntax errors of the JSON metadata and try again.

### What's the `post.md.post2ghost.json` File Used For?

When uploading article `post.md` via Post2Ghost, a file `post.md.post2ghost.json` is created which acts as a _receipt_. It contains the information returned by the Ghost API and is used as the base for all subsequent _updates_ to the same post.

Delete this file if you want to create a new blog post.

### Why Can I Not Publish an Article Straight from Post2Ghost?

More ofen than enough I've discovered flaws when checking the uploaded draft article in Ghost that escaped me when working locally. Silly things like typos, broken links, and overrunning metadata. It just seems to be safer to check the final blog post on the real thing before making it publicly available to the world.

### Which Ghost API Version is Supported by Post2Ghost?

Post2Ghost only supports the [Ghost Public v0.1 API](https://api.ghost.org/v0.1/docs).

### I Know How To Make This Better! How?

Splendid idea as this is work in progress and open source after all!

Feel free to fork, improve, push, and open a pull request so we can eventually merge it back in and make it better for everyone. Thanks!
