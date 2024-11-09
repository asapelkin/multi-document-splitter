#!/usr/bin/env python3

import argparse
import os

import cv2


def get_next_card_number(folder):
    existing_files = [
        f for f in os.listdir(folder) if f.startswith("card_") and f.endswith(".png")
    ]

    numbers = []
    for file in existing_files:
        try:
            num = int(file.split("_")[1].split(".")[0])
            numbers.append(num)
        except ValueError:
            continue

    return max(numbers, default=0) + 1


def main(input_file, output_folder, threshold, padding):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image = cv2.imread(input_file)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, threshold = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY_INV)

    cv2.imwrite(os.path.join(output_folder, "threshold_output.png"), threshold)

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    contour_image = image.copy()

    file_number = get_next_card_number(output_folder)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        aspect_ratio = w / float(h)
        if 1.5 < aspect_ratio < 3.5 and w > 200 and h > 100:
            x_start = max(x - padding, 0)
            y_start = max(y - padding, 0)
            x_end = min(x + w + padding, image.shape[1])
            y_end = min(y + h + padding, image.shape[0])

            card = image[y_start:y_end, x_start:x_end]

            output_path = os.path.join(output_folder, f"card_{file_number+1}.png")
            file_number += 1
            cv2.imwrite(output_path, card)
            print(f"Сохранено: {output_path}")

            cv2.rectangle(
                contour_image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2
            )

    cv2.imwrite(
        os.path.join(output_folder, "contours_output_with_padding.png"), contour_image
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for automatically splitting an image "
        "containing multiple documents into separate images."
    )
    parser.add_argument(
        "--input_file", type=str, required=True, help="Path to the input image."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=250,
        help="Threshold value for image binarization (default is 250).",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=10,
        help="Framing padding.",
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        required=True,
        help="Folder to save the result.",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.input_file, args.output_folder, args.threshold, args.padding)
