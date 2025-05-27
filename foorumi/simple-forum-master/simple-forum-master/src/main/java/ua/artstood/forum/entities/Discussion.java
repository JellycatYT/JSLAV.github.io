package ua.artstood.forum.entities;

import org.hibernate.validator.constraints.Length;

import javax.persistence.*;
import javax.validation.constraints.NotEmpty;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

@Entity
@Table(name = "discussion")
public class Discussion {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "username")
    @Length(min = 6, max = 18, message = "Имя должно быть не короче 6 букв и не длиннее 18")
    @NotEmpty(message = "Имя не должно быть пустым")
    private String username;

    @Column(name = "topic")
    @NotEmpty(message = "Тема не должна быть пустой")
    private String topic;

    @Column(name = "text")
    @NotEmpty(message = "Текст обсуждения не может быть пустым")
    private String text;

    @Column(name="disc_date")
    private Date date;
    //todo comments list

    public Discussion(Long id, String username, String topic, String text, Date date) {
        this.id = id;
        this.username = username;
        this.topic = topic;
        this.text = text;
        this.date = date;
    }

    public Discussion() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getTopic() {
        return topic;
    }

    public void setTopic(String topic) {
        this.topic = topic;
    }

    public String getText() {
        return text;
    }

    public void setText(String text) {
        this.text = text;
    }

    public String commentTime() {
        DateFormat dateFormat = new SimpleDateFormat("MMM dd HH:mm");
        return dateFormat.format(date.getTime());
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

}

