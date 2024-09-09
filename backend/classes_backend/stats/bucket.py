class Bucket:
    def __init__(self, data):
        self.bucket_start = data.get('bucket_start')
        self.bucket_end = data.get('bucket_end')
        self.count = data.get('count')
        self.percentage_of_total = data.get('percentage_of_total')

    def to_dict(self):
        return {
            "bucket_start": self.bucket_start,
            "bucket_end": self.bucket_end,
            "count": self.count,
            "percentage_of_total": self.percentage_of_total
        }