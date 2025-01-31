# **Database Schema**

## 1. User

| Field Name      | Type         | Constraints      |
| --------------- | ------------ | ---------------- |
| id              | UUID (PK)    | Primary Key      |
| username        | String       | Unique, Required |
| email           | String       | Unique, Required |
| password_hash   | String       | Required         |
| profile_picture | String (URL) | Optional         |
| bio             | Text         | Optional         |
| created_at      | Timestamp    | Default: NOW()   |
| updated_at      | Timestamp    | Default: NOW()   |

### Relationships:

- A User can create multiple boards.
- A User can upload multiple posts (images/videos).
- A User can like and comment on multiple posts.

## 2. Board

Field Name Type Constraints
id UUID (PK) Primary Key
name String Required
description Text Optional
user_id UUID (FK) Foreign Key → User
created_at Timestamp Default: NOW()
updated_at Timestamp Default: NOW()

### Relationships:

- A Board can contain multiple posts (images/videos).
- A User can have multiple boards.

3. Post (Previously "Image" - Now Supports Videos Too!)

Relationships:
A Post can belong to one board.
A User can create multiple posts.
A Post can be liked and commented on.

4. Like

Relationships:
A User can like multiple posts.
A Post can have multiple likes.

5. Comment

Relationships:
A User can comment on multiple posts.
A Post can have multiple comments.
A Comment can have nested replies (threaded comments).

6. Follow

Relationships:
A User can follow multiple users.
A User can be followed by multiple users.

Relationships (Updated)
User ↔ Board → A user can create multiple boards.
User ↔ Post → A user can upload multiple posts (images/videos).
Board ↔ Post → A board can contain multiple posts.
User ↔ Like ↔ Post → A user can like multiple posts, and a post can have multiple likes.
User ↔ Comment ↔ Post → A user can comment on multiple posts, and a post can have multiple comments.
Comment ↔ Comment (Threaded) → A comment can have multiple replies (threaded comments).
User ↔ Follow ↔ User → Users can follow other users.
