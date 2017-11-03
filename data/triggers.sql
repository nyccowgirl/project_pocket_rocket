flask signal function that would change database - similar to trigger


CREATE TRIGGER link_friend AFTER UPDATE ON invites FOR EACH ROW WHEN accepted==True
  EXECUTE PROCEDURE link_friend();

CREATE FUNCTION link_friend() RETURNS trigger AS '
  BEGIN
    INSERT INTO friends (user_id, friend_id)
      VALUES (invites.user_id, users.user_id);
  RETURN NEW;
  END;
' LANGUAGE 'plpsql';

-- need to pull in new user_id from users table using email froms invites table