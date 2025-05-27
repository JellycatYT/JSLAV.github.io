package ua.artstood.forum.entities;

import javax.persistence.*;
import javax.validation.constraints.NotEmpty;

@Entity
@Table(name = "comment")
public class Comment {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "dis_id")
    private Long discussionId;

    @NotEmpty(message = "Имя не должно быть пустым")
    @Column(name = "username")
    private String username;

    @Column(name = "text")
    @NotEmpty(message = "Комментарий не может быть пустым")
    private String text;

    public Comment() {
    }

    public Comment(Long discussionId, String username, String text) {
        this.discussionId = discussionId;
        this.username = username;
        this.text = text;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getDiscussionId() {
        return discussionId;
    }

    public void setDiscussionId(Long discussionId) {
        this.discussionId = discussionId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }
}
