# Mixed Correlation Matrix Heatmap with ggplot2
# Lower triangle: Heatmap with correlation values and significance stars
# Upper triangle: Hexagons with size proportional to correlation strength

# Load required libraries
library(tidyverse)
library(ggplot2)
library(reshape2)

# Set seed for reproducibility
set.seed(42)

# ============================================================================
# 1. Generate dummy dataset with meaningful correlations
# ============================================================================
n <- 100
n_vars <- 12

# Create correlated variables
data <- matrix(rnorm(n * n_vars), ncol = n_vars)

# Add correlations between variables
for (i in 2:n_vars) {
  data[, i] <- data[, i] + 0.5 * data[, i-1]
}

# Add some negative correlations
data[, 5] <- data[, 5] - 0.6 * data[, 2]
data[, 8] <- data[, 8] - 0.4 * data[, 3]

# Convert to data frame with variable names
colnames(data) <- paste0("Var", 1:n_vars)
df <- as.data.frame(data)

# ============================================================================
# 2. Calculate correlation matrix and p-values
# ============================================================================

# Correlation matrix
cor_matrix <- cor(df)

# P-value matrix
p_matrix <- matrix(NA, nrow = n_vars, ncol = n_vars)
for (i in 1:n_vars) {
  for (j in 1:n_vars) {
    if (i != j) {
      test <- cor.test(df[, i], df[, j])
      p_matrix[i, j] <- test$p.value
    } else {
      p_matrix[i, j] <- 0
    }
  }
}

# ============================================================================
# 3. Create significance stars
# ============================================================================

get_significance <- function(p) {
  case_when(
    p < 0.001 ~ "***",
    p < 0.01 ~ "**",
    p < 0.05 ~ "*",
    TRUE ~ ""
  )
}

# ============================================================================
# 4. Prepare data for plotting
# ============================================================================

# Convert matrices to long format
cor_long <- melt(cor_matrix)
colnames(cor_long) <- c("Var1", "Var2", "correlation")

p_long <- melt(p_matrix)
colnames(p_long) <- c("Var1", "Var2", "p_value")

# Combine correlation and p-values
plot_data <- cor_long %>%
  left_join(p_long, by = c("Var1", "Var2")) %>%
  mutate(
    significance = get_significance(p_value),
    abs_cor = abs(correlation),
    # Determine position: lower, upper, or diagonal
    position = case_when(
      Var1 == Var2 ~ "diagonal",
      as.numeric(Var1) > as.numeric(Var2) ~ "lower",
      TRUE ~ "upper"
    ),
    # Create label for lower triangle
    label = ifelse(position == "lower" | position == "diagonal",
                   paste0(sprintf("%.2f", correlation), "\n", significance),
                   "")
  )

# ============================================================================
# 5. Create the plot
# ============================================================================

p <- ggplot(plot_data, aes(x = Var2, y = Var1)) +

  # Lower triangle: Heatmap tiles
  geom_tile(data = filter(plot_data, position %in% c("lower", "diagonal")),
            aes(fill = correlation),
            color = "white", size = 0.5) +

  # Lower triangle: Text labels (correlation + significance)
  geom_text(data = filter(plot_data, position %in% c("lower", "diagonal")),
            aes(label = label,
                color = ifelse(abs(correlation) > 0.5, "white", "black")),
            size = 3, fontface = "bold") +

  # Upper triangle: Hexagons with size proportional to correlation strength
  geom_point(data = filter(plot_data, position == "upper"),
             aes(fill = correlation, size = abs_cor),
             shape = 21,  # Circle with fill and border
             color = "white", stroke = 1) +

  # Alternative: Use hexagon shape (requires more complex implementation)
  # For true hexagons, we would need geom_polygon with custom coordinates

  # Color scale: Diverging palette (Blue-White-Red)
  scale_fill_gradient2(
    low = "#d73027",      # Red for negative
    mid = "white",        # White for zero
    high = "#4575b4",     # Blue for positive
    midpoint = 0,
    limits = c(-1, 1),
    name = "Correlation"
  ) +

  # Size scale for upper triangle points
  scale_size_continuous(
    range = c(2, 15),
    limits = c(0, 1),
    name = "Abs(Correlation)"
  ) +

  # Manual color scale for text
  scale_color_identity() +

  # Labels and title
  labs(
    title = "Mixed Correlation Matrix Heatmap",
    subtitle = "Lower: Heatmap with significance (* p<0.05, ** p<0.01, *** p<0.001)\nUpper: Points sized by correlation strength",
    x = NULL,
    y = NULL
  ) +

  # Theme adjustments
  theme_minimal() +
  theme(
    # Remove grid lines
    panel.grid = element_blank(),
    panel.background = element_rect(fill = "white", color = NA),

    # Axis text
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10, face = "bold"),
    axis.text.y = element_text(size = 10, face = "bold"),

    # Title
    plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
    plot.subtitle = element_text(size = 10, hjust = 0.5, color = "gray40"),

    # Legend
    legend.position = "right",
    legend.title = element_text(size = 10, face = "bold"),
    legend.text = element_text(size = 9),

    # Aspect ratio
    aspect.ratio = 1
  ) +

  # Ensure square tiles
  coord_fixed()

# Display the plot
print(p)

# Save the plot
ggsave("mixed_correlation_heatmap.png",
       plot = p,
       width = 12,
       height = 10,
       dpi = 300,
       bg = "white")

cat("Plot saved as 'mixed_correlation_heatmap.png'\n")

# ============================================================================
# Optional: Print correlation statistics
# ============================================================================

cat("\nCorrelation Matrix Summary:\n")
cat("Range:", round(min(cor_matrix[cor_matrix != 1]), 3), "to",
    round(max(cor_matrix[cor_matrix != 1]), 3), "\n")
cat("Mean absolute correlation:",
    round(mean(abs(cor_matrix[upper.tri(cor_matrix)])), 3), "\n")
cat("Significant correlations (p<0.05):",
    sum(p_matrix[upper.tri(p_matrix)] < 0.05, na.rm = TRUE),
    "out of", sum(upper.tri(p_matrix)), "\n")
