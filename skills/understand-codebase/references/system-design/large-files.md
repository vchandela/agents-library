# Large files

Ask first how the bytes can travel straight between the client and object storage. App servers and databases that carry gigabytes waste their network, memory and backups.

## Presigned URLs

Have the server check the user, write a metadata row and sign a short-lived URL, then let the client talk to storage directly. The database holds only a pointer. Proxy through the server instead when files are small or it must inspect content as it arrives. Build the size limit and content type into the signature and let the server pick the key, because anyone holding the URL can use it until it expires. Say who deletes each object, as in "Design the wrong paths and the cleanup" under [First principles](../engineering-principles.md#first-principles). When other people will see uploads, land them somewhere private and publish only after scanning and checking the real file type.

## Upload state from storage events

Mark the row complete from the storage service's own event, never from the client's "done" call, which races and lies. Create the row as pending when you sign the URL. Events can arrive late or not at all, so a periodic job checks stuck rows against storage, and a row left pending forever is recorded and alerted on (see [Errors never go silent](../engineering-principles.md#errors-never-go-silent)).

## Multipart, resumable upload

Split big uploads into parts on the client, never on the server, so a drop late in the upload does not start over. Send the parts straight to storage, which needs each part but the last to be at least about 5 MB, and 5 to 10 MB is a common pick. Key the upload by a content fingerprint so a retry resumes it after a restart. Check the parts with the storage API before completing, and expire unfinished uploads with a lifecycle rule. Downloads need no parts, because range requests already resume. Compress text-like files on the client before upload, but not media that is already compressed, and compress before you encrypt.

## Content-defined chunking

When files change a little at a time, cut chunks where a rolling hash hits a pattern and upload only the chunks storage lacks. Fixed-size chunks fail here, because a small insert moves every boundary after it and every later chunk looks new. Skip it for files that are replaced whole.

## CDN delivery with variants

Serve media many distant users share through a CDN, with sizes and formats made for each device. Chat attachments seen by a few people gain little. Variants cost storage and a processing pipeline, and updates need invalidation. Keep range requests working so downloads resume. For video on shifting networks, cut it into short segments at several bitrates behind a manifest, and transcode them as background jobs (see [long-running work](long-running-work.md)). General cache rules live in [caching](caching.md).
