

party_parrot_url = ("https://ppaas.herokuapp.com/partyparrot?overlay={image_url}&overlayWidth={image_size}"
                    "&overlayHeight={image_size}&overlayOffsetX={x_offset}&overlayOffsetY={y_offset}")


class ParrotUrlGenerator:
    def __init__(self,
                 original_emoji_url: str) -> None:
        self.original_emoji_url = original_emoji_url
        self.image_size = 25
        self.x_offset = -6
        self.y_offset = -12

    def get_emoji_url(self):
        return party_parrot_url.format(image_url=self.original_emoji_url,
                                       image_size=self.image_size,
                                       x_offset=self.x_offset,
                                       y_offset=self.y_offset)
