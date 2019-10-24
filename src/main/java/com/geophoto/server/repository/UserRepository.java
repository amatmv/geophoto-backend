package com.geophoto.server.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Component;
import com.geophoto.server.entity.User;

import java.util.List;

@Component
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT u FROM users u WHERE u.username=:username")
    List<User> findByUsername(@Param("username") String username);
}
