package pl.portfolio.clothingsimilarity.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import pl.portfolio.clothingsimilarity.model.ClothingItem;

public interface ClothingItemRepository extends MongoRepository<ClothingItem, String> {
    // Add custom query methods if needed
}