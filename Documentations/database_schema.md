# **DATABASE SCHEMA**

## 1. User

    Fields:

        1. id (Primary Key)
        2. username (Unique)
        3. email (Unique)
        4. password_hash
        5. profile_picture (Optional)
        6. bio (Optional)
        7. created_at
        8. updated_at

## 2. Board

    Fields:

        1. id (Primary Key)
        2. name
        3. description (Optional)
        4. user_id (Foreign Key: Links to User table)
        5. created_at
        6. updated_at

## 3. Image

    Fields:

        1. id (Primary Key)
        2. title
        3. description (Optional)
        4. image_url (URL to the image file)
        5. board_id (Foreign Key: Links to Board table)
        6. user_id (Foreign Key: Links to User table)
        7. created_at
        8. updated_at

## 4. Like

    Fields:

        1. id (Primary Key)
        2. user_id (Foreign Key: Links to User table)
        3. image_id (Foreign Key: Links to Image table)
        4. created_at

## 5. Comment

    Fields:

        1. id (Primary Key)
        2. user_id (Foreign Key: Links to User table)
        3. image_id (Foreign Key: Links to Image table)
        4. parent_comment_id (Nullable, Foreign Key: Links to Comment table for threaded comments)
        5. content (Text)
        6. created_at
        7. updated_at

## 6. Threaded Comment (Reply to Comment)

    Fields:

        1. id (Primary Key)
        2. parent_comment_id (Foreign Key: Links to Comment table)
        3. user_id (Foreign Key: Links to User table)
        4. content (Text)
        5. created_at
        6. updated_at

## Relationships:

    1. User ↔ Board: A user can create many boards.
    2. User ↔ Image: A user can upload many images.
    3. Board ↔ Image: A board can contain many images.
    4. User ↔ Like ↔ Image: A user can like many images, and an image can have many likes.
    5. User ↔ Comment ↔ Image: A user can comment on many images, and an image can have many comments.
    6. Comment ↔ Comment (Threaded): A comment can have multiple replies (threaded comments).
