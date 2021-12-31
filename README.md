# wikidot-forum-dump

Script is partially based on 2stacks by bluesoul: https://github.com/scuttle/2stacks

To dump a Wiki's forum, edit `config.py` and put the required Wiki name (default — `scp-wiki`, which is the SCP EN community).

If your forum is too large, you may edit `threads` parameter in `config.py`, however make sure you don't overload Wikidot with requests — no one knows what that may result in.

Then make sure you have the following Python packages:

```
beautifulsoup4
```

Run `python .` to start dumping.

**Note:** incremental dump (i.e. updating existing categories or threads) is not supported.

However, if the process is interrupted at any point, it can be seamlessly resumed per-category and per-thread.

The dump will be stored under the following structure:

```
dump/
  categories.json           -- contains group and category names and IDs
  categories/
    <category_id>.json      -- contains list of threads for each category by ID
  threads/
    <thread_id>.json        -- contains each thread with all posts and replies
```

Example of a group+categories record (from SCP-EN):
```json
{
    "title": "Site Announcements and Proposals",
    "description": "Announce new pages, suggest policy, and interact with new site members.",
    "categories": [
      {
        "title": "Sitewide Announcements",
        "description": "Announcement of any sitewide changes or events. For usage by both staff and non-staff.",
        "id": 1113520
      },
      {
        "title": "Page Announcements",
        "description": "Announce posting of new pages and deletion of old pages. Authors, please use the collective SCP, Tale, GOI Entry, and Update threads for new works.",
        "id": 7409511
      },
      {
        "title": "Proposals And Policy",
        "description": "What can we do to improve the site? Ask any questions you may have regarding site structure and policy.",
        "id": 51015
      },
      {
        "title": "Introductions",
        "description": "New to the site? Introduce yourself and meet other site members here.",
        "id": 72352
      }
    ]
  }
```

Example of a thread record (also from SCP-EN):

```json
{
  "breadcrumbs": [
    "Forum",
    "Site Announcements and Proposals / Sitewide Announcements",
    "Technical Issues Announcement"
  ],
  "category": 1113520,
  "base_page_id": null,
  "description": "An announcement regarding some Wikidot technical difficulties and mitigations, with particular reference to file uploads.",
  "user": {
    "avatar": "http://www.wikidot.com/avatar.php?userid=3075960&amp;size=small&amp;timestamp=1640941899",
    "name": "stormbreath",
    "id": 3075960
  },
  "date": 1640899718,
  "posts": [
    {
      "user": {
        "avatar": "http://www.wikidot.com/avatar.php?userid=3075960&amp;size=small&amp;timestamp=1640941899",
        "name": "stormbreath",
        "id": 3075960
      },
      "date": 1640899718,
      "title": "Technical Issues Announcement",
      "content": "<p>Hey everyone.</p>\n<p>Currently, we're having some Wikidot problems with the Master Admin position. We've moved the Master Admin position to a different account (under Mann's control) in the meantime, but there may be problems for a few days while we sort things out.</p>\n<p>The thing most prominently affected by this will be uploaded files. Until the issue is resolved, please host images on an external hosting site like <a href=\"https://imgur.com/\">Imgur</a>. After image uploading has resumed functioning, Staff will reupload the images on the mainsite manually. This will affect the sandbox as well.</p>\n<p>Helen (our IRC bot) will also be temporarily down until the problem has been resolved. This also means some Helen-adjacent functions may not be functional, or may experience issues.</p>\n<p>We thank you for your cooperation during this. If you have any questions about the above or any other problems you come across, feel free to ask in this thread or message a staff member. Thank you.</p>",
      "replies": [
        {
          "user": {
            "avatar": "http://www.wikidot.com/avatar.php?userid=3695324&amp;size=small&amp;timestamp=1640941899",
            "name": "CephalopodStevenson",
            "id": 3695324
          },
          "date": 1640903834,
          "title": "Re: Technical Issues Announcement",
          "content": "<p>So, I’ll preface by saying that I have very little knowledge of how wikidot works. I hope somebody can enlighten me here and explain what any of this means. Why does a master admin problem affect media files? What exactly is the problem? Who was controlling the master admin account before, and is this an issue with said user or wikidot itself?</p>\n<p>Also, “most prominently affected” suggests that there may be other concerns, right? I’m guessing this means we should be backing up our content regardless of media inserts. Again, I’m not super knowledgeable on any of this, so if someone could clarify a bit, I’d appreciate it.</p>",
          "replies": [
            {
              "user": {
                "avatar": "http://www.wikidot.com/avatar.php?userid=2005044&amp;size=small&amp;timestamp=1640941899",
                "name": "Decibelles",
                "id": 2005044
              },
              "date": 1640905152,
              "title": "Re: Technical Issues Announcement",
              "replies": [],
              "content": "<blockquote>\n<p>Why does a master admin problem affect media files? What exactly is the problem? Who was controlling the master admin account before, and is this an issue with said user or wikidot itself?</p>\n</blockquote>\n<p>This one's a bit of a tricky one to explain, as the answers are all interconnected. The Master Admin before was Mann. Mann has a Pro account. <a href=\"http://www.wikidot.com/plans\">Wikidot's subscription plans</a> allow a site to have a bunch of features that you cannot have if you make a site with a Free account. Among these features is an upgrade in storage space, IE, how much you can upload to a site. In addition to this, you can also buy more storage as well.</p>\n<p>The master admin status presumably has shifted from Mann to another account, still under Mann's control. However, this other account presumably does not have Pro. So therefore, storage limits will have naturally been hit. I can't pretend to know what the issue was that resulted in the transfer of status, but this would end up resulting in storage now being at a premium until the situation can be resolved.</p>\n<blockquote>\n<p>I’m guessing this means we should be backing up our content regardless of media inserts.</p>\n</blockquote>\n<p>I'm not sure what anything else affected could be, but it is 100% always a good idea to back up your content from this site as best as you are able to.</p>"
            },
            {
              "user": {
                "avatar": "http://www.wikidot.com/avatar.php?userid=2199269&amp;size=small&amp;timestamp=1640941899",
                "name": "Yossipossi",
                "id": 2199269
              },
              "date": 1640905211,
              "title": "Re: Technical Issues Announcement",
              "content": "<p><span style=\"white-space: pre-wrap;\"> </span></p>\n<div style=\"text-align: center;\">\n<div class=\"collapsible-block\">\n<div class=\"collapsible-block-folded\"><a class=\"collapsible-block-link\" href=\"javascript:;\">+ Collapsed Response b/c of Length +</a></div>\n<div class=\"collapsible-block-unfolded\" style=\"display:none\">\n<div class=\"collapsible-block-unfolded-link\"><a class=\"collapsible-block-link\" href=\"javascript:;\">- Hide -</a></div>\n<div class=\"collapsible-block-content\">\n<div style=\"text-align: left;\">\n<blockquote>\n<p>Why does a master admin problem affect media files?</p>\n</blockquote>\n<p>As we are transferring the Master Admin permission to a separate account without Pro Plus, until the new account can receive Pro Plus, we will have reduced image size for the Wiki. Thus, no new images can be uploaded.</p>\n<blockquote>\n<p>What exactly is the problem?</p>\n</blockquote>\n<p>The exact issue we are trying to solve will not be disclosed at this time, however it is related to a Wikidot issue.</p>\n<blockquote>\n<p>Who was controlling the master admin account before, and is this an issue with said user or wikidot itself?</p>\n</blockquote>\n<p>Mann was, and still is, Master Admin. The account was changed from <span class=\"printuser avatarhover\"><a href=\"http://www.wikidot.com/user:info/dreverettmann\" onclick=\"WIKIDOT.page.listeners.userInfo(323946); return false;\"><img alt=\"DrEverettMann\" class=\"small\" src=\"http://www.wikidot.com/avatar.php?userid=323946&amp;amp;size=small&amp;amp;timestamp=1640905211\" style=\"background-image:url(http://www.wikidot.com/userkarma.php?u=323946)\"/></a><a href=\"http://www.wikidot.com/user:info/dreverettmann\" onclick=\"WIKIDOT.page.listeners.userInfo(323946); return false;\">DrEverettMann</a></span> to a separate alt, which is still under Mann's control. This is solely a Wikidot problem.</p>\n<blockquote>\n<p>Also, “most prominently affected” suggests that there may be other concerns, right? I’m guessing this means we should be backing up our content regardless of media inserts.</p>\n</blockquote>\n<p>It is recommended to back up your articles regardless (Wikidot may go under at any moment, of course, but that's not new information). Other affected things are related to the alt's lack of Pro Plus (for the time being), such as HTTP instead of HTTPS and login issues for some users.</p>\n</div>\n</div>\n<div class=\"collapsible-block-unfolded-link\"><a class=\"collapsible-block-link\" href=\"javascript:;\">- Hide -</a></div>\n</div>\n</div>\n</div>\n<br/>\n<span style=\"white-space: pre-wrap;\"> </span>",
              "replies": [
                {
                  "user": {
                    "avatar": "http://www.wikidot.com/avatar.php?userid=3695324&amp;size=small&amp;timestamp=1640941899",
                    "name": "CephalopodStevenson",
                    "id": 3695324
                  },
                  "date": 1640905510,
                  "title": "Re: Technical Issues Announcement",
                  "replies": [],
                  "content": "<p>Thanks both of you for the informative responses. I feel I have a much better understanding of the situation now.</p>"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Note**: contrarily to what it says, `base_page_id` is not an ID, but a slug (e.g. `scp-173`).

This exists only for page discussion threads.
