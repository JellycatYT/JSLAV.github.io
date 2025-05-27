package ua.artstood.forum.repositiories;

import org.springframework.data.repository.CrudRepository;

import org.springframework.stereotype.Repository;
import ua.artstood.forum.entities.Comment;

import java.util.List;

@Repository
public interface CommentsRepository extends CrudRepository<Comment,Long> {
    List<Comment> findAllByDiscussionId(Long discussionId);
    void deleteAllByDiscussionId(Long discussionId);
}
