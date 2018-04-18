/*
 * Ensure active users have a confirmed_at date set.
 */

var count = 0;

db.user.find({active: true, confirmed_at: null}).forEach(function(user) {
    user.confirmed_at = Date();
    db.user.save(user);
    count++;
});

print(`${count} users migrated.`);
