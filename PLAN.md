# Plan

## Problem (as given)
> Our marketing team shares a lot of links: in emails, on social, in printed flyers. The URLs are long and ugly, and right now they have no idea which links actually get clicked. We’d like you to build a link shortener for them.

## Clarifying questions and answers
- Who is the user / core action? -> marketing team, 10 people, internal
- What does "done" look like at the end? -> working prototype, has a visual component, can generate urls and stores a mapping of generate urls to the shortened version in the database. The shortened link needs to redirect to the original link. the number of clicks are recorded per link.
- Persistence needed? Multi-user / auth? (default: single hardcoded user) -> persistance would be good, its internal so no login needed.
- Scale: rough number of items? -> ~100s of links, 1000s of clicks/hour burst, one server
- Real-time / con
current editing? -> rely on UNIQUE constraint + retry
- External APIs? Can I mock them? -> none
- Expiry? -> no, links are permanent (printed flyers)
- Delete? -> yes. Soft delete, hides deleted links and returns an error when trying to reach

## Scope
**Building (MVP):**
1. Create a shortened link from a longer URL (generate slug)
2. Record clicks on valid slugs, faulty or deleted slugs returns an error
3. UI provides a table/form that shows shortened link, original link, click count, and delete button
4. Deleting a URL hides it from the list and adds it to a hidden list so if queried, returns an error. 

**Skipping (and why):**
-

**Stretch, if time allows:**
- Custom URLS, allows users to generate a custom url given that it is not already in use.


## Edge cases to handle
-

## Known limitations / what I'd do next
-