package pl.portfolio.clothingsimilarity.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import pl.portfolio.clothingsimilarity.model.ClothingItem;

import java.util.List;

@RestController
@RequestMapping("/api/images")
public class ImageController {

    @PostMapping("/upload")
    public ResponseEntity<String> uploadImage(@RequestParam("file") MultipartFile file) {
        // Implement the logic to handle image upload and save it to the file system or database
        // You can use the MultipartFile object to access the uploaded image data
        // Return an appropriate response based on the result
        return ResponseEntity.ok("Image uploaded successfully");
    }

    @GetMapping("/similar")
    public ResponseEntity<List<ClothingItem>> getSimilarImages(@RequestParam("imageUrl") String imageUrl) {
        // Implement the logic to search for similar images based on the provided imageUrl
        // Use the MongoDB repository to query the database and retrieve the similar images
        // Return the list of similar images as a response
        return ResponseEntity.ok(List.of());
    }

}

