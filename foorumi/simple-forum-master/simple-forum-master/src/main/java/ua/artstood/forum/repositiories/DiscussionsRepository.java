package ua.artstood.forum.repositiories;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;
import ua.artstood.forum.entities.Discussion;

@Repository
public interface DiscussionsRepository extends CrudRepository<Discussion, Long> {
}
