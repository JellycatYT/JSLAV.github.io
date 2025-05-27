package ua.artstood.forum.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ModelAttribute;

import ua.artstood.forum.entities.Comment;
import ua.artstood.forum.entities.Discussion;
import ua.artstood.forum.repositiories.CommentsRepository;
import ua.artstood.forum.repositiories.DiscussionsRepository;

import javax.transaction.Transactional;
import javax.validation.Valid;
import java.util.Date;

@Controller
@RequestMapping("discussions")
public class DiscussionsController {

    private final DiscussionsRepository discussionsRepository;
    private final CommentsRepository commentsRepository;

    @Autowired
    public DiscussionsController(DiscussionsRepository discussionsRepository, CommentsRepository commentsRepository) {
        this.commentsRepository = commentsRepository;
        this.discussionsRepository = discussionsRepository;
    }

    @GetMapping()
    public String showAllEntries(Model model) {
        model.addAttribute("discussions", discussionsRepository.findAll());
        return "discussions/discussions";
    }

    @GetMapping("{id}")
    public String showSpecificEntry(@PathVariable long id, Model model) {
        model.addAttribute("discussion", discussionsRepository.findById(id).get());
        model.addAttribute("comments", commentsRepository.findAllByDiscussionId(id));
        return "discussions/specific_discussion";
    }

    @GetMapping("new")
    public String newDiscussion(@ModelAttribute("discussion") Discussion discussion) {
        return "discussions/new";
    }

    @PostMapping()
    public String addNewDiscussion(@ModelAttribute("discussion") @Valid Discussion discussion,
                                   BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return "discussions/new";
        }
        discussion.setDate(new Date());
        discussionsRepository.save(discussion);
        return "redirect:/discussions";
    }

    @GetMapping("{id}/edit")
    public String editForm(Model model, @PathVariable("id") long id) {
        model.addAttribute("discussion", discussionsRepository.findById(id).get());
        return "discussions/edit";
    }

    @PatchMapping("{id}")
    public String edit(@PathVariable("id") long id,
                       @ModelAttribute("discussion") @Valid Discussion discussion,
                       BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return "discussions/edit";
        }
        //forumDAO.update(id, discussion);
        Discussion oldDis = discussionsRepository.findById(id).get();
        oldDis.setText(discussion.getText());
        oldDis.setTopic(discussion.getTopic());
        oldDis.setUsername(discussion.getUsername());
        discussionsRepository.save(oldDis);

        return "redirect:/discussions";
    }

    @Transactional
    @DeleteMapping("{id}")
    public String delete(@PathVariable("id") long id) {
        discussionsRepository.deleteById(id);
        commentsRepository.deleteAllByDiscussionId(id);
        return "redirect:/discussions";
    }
    @GetMapping("{dis_id}/new")
    public String newCommentForm(@ModelAttribute("comment") Comment comment, @PathVariable("dis_id") int dis_id){
        return "comments/new";
    }

    @PostMapping("{dis_id}")
    public String createComment( @ModelAttribute("comment") @Valid Comment comment,
                                BindingResult bindingResult,
                                @PathVariable("dis_id") long dis_id) {
        if (bindingResult.hasErrors()) {
            return "redirect:/comments/new";
        }
        comment.setDiscussionId(dis_id);
        commentsRepository.save(comment);
        return "redirect:/discussions/{dis_id}";
    }
}
