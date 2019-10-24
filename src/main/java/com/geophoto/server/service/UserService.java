package com.geophoto.server.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.geophoto.server.entity.User;
import com.geophoto.server.repository.UserRepository;

import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public UserRepository crud() {
        return userRepository;
    }

    public User getUser(Long id) {
        Optional<User> uo = userRepository.findById(id);
        if (uo.isPresent())
            return uo.get();
        else
            return null;
    }

    public User getUserProfile(long id) {
        return this.getUser(id);
    }

    @Transactional
    public void setUsername(Long userId, String username) {
        User u = this.getUser(userId);
        if (u != null) {
            u.setUsername(username);
            userRepository.saveAndFlush(u);
        }
    }
    @Transactional
    public void setFullName(Long userId, String fullName) {
        User u = this.getUser(userId);
        if (u != null) {
            u.setFullName(fullName);
            userRepository.saveAndFlush(u);
        }
    }
    @Transactional
    public void setEmail(Long userId, String email) {
        User u = this.getUser(userId);
        if (u != null) {
            u.setEmail(email);
            userRepository.saveAndFlush(u);
        }
    }
    @Transactional
    public void setPassword(Long userId, String password) {
        User u = this.getUser(userId);
        if (u != null) {
            u.setPassword(password);
            userRepository.saveAndFlush(u);
        }
    }

    public void deleteUser(Long userId){
        userRepository.deleteById(userId);
    }
}

